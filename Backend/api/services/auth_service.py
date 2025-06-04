# services/auth_service.py
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
import random
import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))

def get_client_ip(request) -> str:
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def initiate_signup(user_data: Dict[str, Any], request) -> Dict[str, Any]:
    """
    Initiate user signup process by generating verification code and sending email
    """
    try:
        email = user_data['email'].lower()
        full_name = user_data['full_name']
        code = generate_verification_code()
        
        # Store user data in cache with timestamp
        cache_data = {
            'full_name': full_name,
            'email': email,
            'phone_number': user_data.get('phone_number', ''),
            'password':  user_data['password'], # ✅ Plain text; will be hashed properly in .set_password()
            'code': code,
            'timestamp': timezone.now().timestamp(),
            'attempts': 0
        }
        
        # Cache for 10 minutes
        cache.set(f'signup_{email}', json.dumps(cache_data), timeout=600)
        
        # Send verification email
        email_sent = send_verification_email(email, full_name, code)
        
        if email_sent:
            return {'success': True}
        else:
            return {'success': False, 'error': 'Failed to send verification email.'}
            
    except Exception as e:
        logger.error(f"Error initiating signup: {str(e)}")
        return {'success': False, 'error': 'Failed to process signup request.'}

def send_verification_email(email: str, name: str, code: str) -> bool:
    """
    Send verification email with HTML template
    """
    try:
        subject = 'Verify Your RideBolt Account'
        
        # Context for email template
        context = {
            'name': name,
            'code': code,
            'app_name': 'RideBolt',
            'support_email': settings.DEFAULT_FROM_EMAIL
        }
        
        # Try to use HTML template if available
        try:
            html_content = render_to_string('emails/verification_email.html', context)
            text_content = strip_tags(html_content)
        except:
            # Fallback to simple text email
            text_content = f"""
Hi {name},

Welcome to RideBolt! 

Please use the verification code below to verify your email address:

🔐 Verification Code: {code}

This code will expire in 10 minutes.

If you didn't create an account with us, you can safely ignore this email.

Best regards,
The RideBolt Team

---
Need help? Contact us at {settings.DEFAULT_FROM_EMAIL}
            """.strip()
            html_content = None
        
        # Create email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send(fail_silently=False)
        logger.info(f"Verification email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending verification email to {email}: {str(e)}")
        return False

def resend_verification_code(email: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resend verification code for pending signup
    """
    try:
        # Generate new code
        new_code = generate_verification_code()
        
        # Update cached data
        user_data['code'] = new_code
        user_data['timestamp'] = timezone.now().timestamp()
        user_data['attempts'] = user_data.get('attempts', 0) + 1
        
        # Update cache
        cache.set(f'signup_{email}', json.dumps(user_data), timeout=600)
        
        # Send new verification email
        email_sent = send_verification_email(email, user_data['full_name'], new_code)
        
        if email_sent:
            return {'success': True}
        else:
            return {'success': False, 'error': 'Failed to send verification email.'}
            
    except Exception as e:
        logger.error(f"Error resending verification code: {str(e)}")
        return {'success': False, 'error': 'Failed to resend verification code.'}

def send_password_reset_email(email: str, name: str, reset_token: str) -> bool:
    """
    Send password reset email
    """
    try:
        subject = 'Reset Your RideBolt Password'
        
        # Create reset URL (adjust based on your frontend)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        context = {
            'name': name,
            'reset_url': reset_url,
            'app_name': 'RideBolt',
            'support_email': settings.DEFAULT_FROM_EMAIL
        }
        
        try:
            html_content = render_to_string('emails/password_reset_email.html', context)
            text_content = strip_tags(html_content)
        except:
            text_content = f"""
Hi {name},

You recently requested to reset your password for your RideBolt account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request a password reset, you can safely ignore this email.

Best regards,
The RideBolt Team

---
Need help? Contact us at {settings.DEFAULT_FROM_EMAIL}
            """.strip()
            html_content = None
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send(fail_silently=False)
        logger.info(f"Password reset email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending password reset email to {email}: {str(e)}")
        return False

def send_welcome_email(email: str, name: str) -> bool:
    """
    Send welcome email after successful signup
    """
    try:
        subject = 'Welcome to RideBolt!'
        
        context = {
            'name': name,
            'app_name': 'RideBolt',
            'login_url': f"{settings.FRONTEND_URL}/login",
            'support_email': settings.DEFAULT_FROM_EMAIL
        }
        
        try:
            html_content = render_to_string('emails/welcome_email.html', context)
            text_content = strip_tags(html_content)
        except:
            text_content = f"""
Hi {name},

Welcome to RideBolt! 🚗

Your account has been successfully created and verified. You can now start using our ride-sharing platform.

Get started: {settings.FRONTEND_URL}/login

Features you can explore:
• Book rides instantly
• Track your driver in real-time
• Rate and review your experience
• Manage your payment methods

If you have any questions, don't hesitate to reach out to our support team.

Best regards,
The RideBolt Team

---
Need help? Contact us at {settings.DEFAULT_FROM_EMAIL}
            """.strip()
            html_content = None
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send(fail_silently=False)
        logger.info(f"Welcome email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending welcome email to {email}: {str(e)}")
        return False
    

