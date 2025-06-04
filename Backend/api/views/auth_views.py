# views/auth_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import socket
import smtplib
import dns.resolver
import logging
from datetime import timedelta

from ..models.user_model import User
from ..serializers.signupSerializer import SignupSerializer
from ..serializers.loginSerializer import LoginSerializer
from ..services import auth_service
from ..utils.rate_limiting import check_rate_limit
from ..utils.validators import validate_password_strength

logger = logging.getLogger(__name__)

@api_view(['POST'])
def signup(request):
    """
    User registration endpoint with email verification
    """
    try:
        # Rate limiting check
        client_ip = auth_service.get_client_ip(request)
        if not check_rate_limit(f'signup_{client_ip}', max_attempts=5, window_minutes=15):
            return Response(
                {'error': 'Too many signup attempts. Please try again later.'}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'An account with this email already exists.'}, 
                status=status.HTTP_409_CONFLICT
            )
        
        # Validate password strength
        password_errors = validate_password_strength(password)
        if password_errors:
            return Response(
                {'error': 'Password does not meet requirements.', 'details': password_errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if there's already a pending verification
        cached_data = cache.get(f'signup_{email}')
        if cached_data:
            cached_user_data = json.loads(cached_data)
            time_since_last = timezone.now().timestamp() - cached_user_data.get('timestamp', 0)
            if time_since_last < 60:  # 1 minute cooldown
                return Response(
                    {'error': 'Please wait before requesting another verification code.'}, 
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
        
        # Generate and send verification code
        result = auth_service.initiate_signup(serializer.validated_data, request)
        if result['success']:
            return Response(
                {'message': 'Verification code sent to your email. Please check your inbox.'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': result['error']}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    Email verification endpoint
    """
    try:
        email = request.data.get('email', '').lower().strip()
        code = request.data.get('code', '').strip()
        
        if not email or not code:
            return Response(
                {'error': 'Email and verification code are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rate limiting for verification attempts
        client_ip = auth_service.get_client_ip(request)
        rate_limit_key = f'verify_{email}_{client_ip}'
        if not check_rate_limit(rate_limit_key, max_attempts=5, window_minutes=15):
            return Response(
                {'error': 'Too many verification attempts. Please try again later.'}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Get cached signup data
        cached_data = cache.get(f'signup_{email}')
        if not cached_data:
            return Response(
                {'error': 'No pending signup found or verification code expired.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_data = json.loads(cached_data)
        
        # Verify code
        if user_data.get('code') != code:
            return Response(
                {'error': 'Invalid verification code.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if code is expired (10 minutes)
        code_timestamp = user_data.get('timestamp', 0)
        if timezone.now().timestamp() - code_timestamp > 600:  # 10 minutes
            cache.delete(f'signup_{email}')
            return Response(
                {'error': 'Verification code has expired. Please signup again.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Double-check user doesn't exist
        if User.objects.filter(email=email).exists():
            cache.delete(f'signup_{email}')
            return Response(
                {'error': 'An account with this email already exists.'}, 
                status=status.HTTP_409_CONFLICT
            )
        
        # Create user atomically
        with transaction.atomic():
            user = User(
                full_name=user_data['full_name'],
                email=email,
                phone_number=user_data.get('phone_number', ''),
                email_verified=True,
                created_at=timezone.now()
            )
            user.set_password(user_data['password'])
            user.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Clear cache
            cache.delete(f'signup_{email}')
            
            logger.info(f"User created successfully: {email}")
            
            return Response({
                'message': 'Account created and email verified successfully.',
                'user': {
                    'id': user.id,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone_number': user.phone_number
                },
                'tokens': {
                    'access': str(access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try:
        client_ip = auth_service.get_client_ip(request)
        email = request.data.get('email', '').lower().strip()
        rate_limit_key = f'login_{email}_{client_ip}'

        if not check_rate_limit(rate_limit_key, max_attempts=5, window_minutes=15):
            return Response({'error': 'Too many login attempts. Please try again later.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        if not user.email_verified:
            return Response({'error': 'Please verify your email before logging in.'},
                            status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            return Response({'error': 'Your account has been deactivated. Please contact support.'},
                            status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'last_login': user.last_login.isoformat() if user.last_login else None
            },
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password.'},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return Response({'error': 'An unexpected error occurred. Please try again.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def logout(request):
    """
    User logout endpoint - blacklist refresh token
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
        return Response(
            {'message': 'Logged out successfully.'}, 
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response(
            {'error': 'An error occurred during logout.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    """
    Resend verification code
    """
    try:
        email = request.data.get('email', '').lower().strip()
        if not email:
            return Response(
                {'error': 'Email is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rate limiting
        client_ip = auth_service.get_client_ip(request)
        rate_limit_key = f'resend_{email}_{client_ip}'
        if not check_rate_limit(rate_limit_key, max_attempts=3, window_minutes=15):
            return Response(
                {'error': 'Too many resend attempts. Please try again later.'}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Check if there's pending signup
        cached_data = cache.get(f'signup_{email}')
        if not cached_data:
            return Response(
                {'error': 'No pending signup found for this email.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_data = json.loads(cached_data)
        
        # Generate new code and send email
        result = auth_service.resend_verification_code(email, user_data)
        if result['success']:
            return Response(
                {'message': 'New verification code sent to your email.'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': result['error']}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Resend verification error: {str(e)}")
        return Response(
            {'error': 'An unexpected error occurred. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
'''
This part of the code verifies the existence of an email address by checking its format, domain, and SMTP server.
'''
@api_view(['POST'])
def verify_email_api(request):

    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Step 1: Format validation
        validate_email(email)
        
        # Step 2: Domain and MX check
        domain = email.split('@')[1]
        mx_exists = check_mx_record(domain)
        
        # Check if it exists in database 
        User.objects.filter(email=email).exists()
        if User.objects.filter(email=email).exists():
            return Response({
                'email': email,
                'valid': False,
                'reason': 'Email exists in database'
            })
        if not mx_exists:
            return Response({
                'email': email,
                'valid': False,
                'reason': 'Domain has no MX record'
            })
        
        # Step 3: SMTP verification
        smtp_valid = verify_smtp(email, domain)
        
        return Response({
            'email': email,
            'valid': smtp_valid,
            'reason': 'Email exists' if smtp_valid else 'Email does not exist'
        })
        
    except ValidationError:
        return Response({
            'email': email,
            'valid': False,
            'reason': 'Invalid email format'
        })
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        return Response(
            {'error': 'Verification failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def check_mx_record(domain):
    """Check if domain has MX record"""
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

def verify_smtp(email, domain):
    """Verify email via SMTP"""
    try:
        # Get MX record
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0]).split(' ')[1].rstrip('.')
        
        # Connect and verify
        with smtplib.SMTP(mx_record, timeout=10) as server:
            server.helo('example.com')
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            return code == 250
            
    except Exception as e:
        logger.warning(f"SMTP check failed for {email}: {str(e)}")
        return False



