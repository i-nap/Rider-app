from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class User(models.Model):
    """
    Represents a user in the system with personal and authentication information.
    """
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=120, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    profile_photo_url = models.URLField(max_length=500, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Added this field
    last_login = models.DateTimeField(null=True, blank=True)  # Added this field
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # The relationships are defined in the Group model:
    # admin_groups = related_name from the admin ForeignKey in Group
    # member_groups = related_name from the members ManyToManyField in Group

    def __str__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

    def set_password(self, password):
        """
        Securely hash and store the user's password.
        """
        self.password = make_password(password)

    def check_password(self, password):
        """
        Check the provided password against the stored hash.
        """
        print("Checking password:", password, "against stored hash:", self.password)
        return check_password(password, self.password)

    def to_dict(self, include_sensitive=False, include_groups=False):
        """
        Serialize the user instance to a dictionary.
        """
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "profile_photo_url": self.profile_photo_url,
            "is_active": self.is_active,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data["password"] = self.password
            
        if include_groups:
            data["admin_groups"] = [group.to_dict() for group in self.admin_groups.all()]
            data["member_groups"] = [
                {
                    "group": membership.group.to_dict(),
                    "joined_at": membership.joined_at.isoformat() if membership.joined_at else None,
                    "is_active": membership.is_active
                }
                for membership in self.groupmembership_set.all()
            ]
            
        return data