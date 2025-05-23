from django.db import models
from django.utils import timezone

class Group(models.Model):
    """
    Represents a user-created travel group with location data and timing.
    """
    name = models.CharField(max_length=100, unique=True)
    admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='admin_groups')
    members = models.ManyToManyField('User', through='GroupMembership', related_name='member_groups')
    
    start_latitude = models.FloatField()
    start_longitude = models.FloatField()
    dest_latitude = models.FloatField()
    dest_longitude = models.FloatField()
    
    start_date = models.DateTimeField()
    expected_end_date = models.DateTimeField()
    member_count = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    joining_code = models.FloatField(unique=True, null=True, blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"<Group(id={self.id}, name='{self.name}', admin_id={self.admin.id if self.admin else None})>"

    def to_dict(self, include_admin=False, include_members=False):
        data = {
            "id": self.id,
            "name": self.name,
            "admin_id": self.admin.id,
            "start_latitude": self.start_latitude,
            "start_longitude": self.start_longitude,
            "dest_latitude": self.dest_latitude,
            "dest_longitude": self.dest_longitude,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "expected_end_date": self.expected_end_date.isoformat() if self.expected_end_date else None,
            "member_count": self.member_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_admin:
            data["admin"] = self.admin.to_dict() if self.admin else None
            
        if include_members:
            data["members"] = [membership.user.to_dict() for membership in self.groupmembership_set.all()]
            
        return data


class GroupMembership(models.Model):
    """
    Represents a membership relationship between a User and a Group,
    with additional metadata about the membership.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    last_location_latitude = models.FloatField(null=True, blank=True)
    last_location_longitude = models.FloatField(null=True, blank=True)
    last_location_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'group')
        
    def __str__(self):
        return f"<GroupMembership(user_id={self.user.id}, group_id={self.group.id})>"
    
    def to_dict(self):
        return {
            "user_id": self.user.id,
            "group_id": self.group.id,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "is_active": self.is_active,
            "last_location_latitude": self.last_location_latitude,
            "last_location_longitude": self.last_location_longitude,
            "last_location_updated": self.last_location_updated.isoformat() if self.last_location_updated else None
        }