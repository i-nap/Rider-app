from django.core.exceptions import ObjectDoesNotExist
from api.models.group_model import Group, GroupMembership
from api.models.user_model import User
from datetime import timedelta
import math
from django.utils import timezone
import random

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth using the Haversine formula.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def getCompleteListGroups(longitude=None, latitude=None):
    """
Sort the list ani then return it to the view    """
    try:
        groups = Group.objects.all()
        # Check date if start bhako bhaye don't include it 
        # Filter out groups that have already started
        groups = [group for group in groups if group.start_date > timezone.now()]
        if longitude is not None and latitude is not None:
            groups_with_distance = []
            for group in groups:
                if group.start_latitude is not None and group.start_longitude is not None:
                    distance = haversine(latitude, longitude, group.start_latitude, group.start_longitude)
                    groups_with_distance.append((distance, group))
            # Sort by distance
            sorted_groups = [group for distance, group in sorted(groups_with_distance, key=lambda x: x[0])]
            return sorted_groups
        return list(groups)
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def join_group(group_id, userid):
 
    try:
        group = Group.objects.get(id=group_id)
        if not group.private:
            group.member_count += 1
            group.save()
            if group.admin.id == userid:
                raise Exception("You cannot join your own group")
            userData = User.objects.get(id=userid)
            if userData in group.members.all():
                print(group.members.all())

                raise Exception("You are already a member of this group")
            group.members.add(userData)
            return group
        else:
            raise Exception("This group is private. Please enter the joining code.") 
    except ObjectDoesNotExist:
        raise Exception("Group does not exist")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}") 

def getMyGroupList(user_id):
    try:
        user = User.objects.get(id=user_id)
        
        memberships = GroupMembership.objects.filter(user=user)
        
        groups_list = []
        for membership in memberships:
            group = membership.group
            group_dict = group.to_dict()
            
            # Add membership specific information
            group_dict.update({
                'is_admin': (group.admin_id == user_id),
                'joined_at': membership.joined_at.isoformat() if membership.joined_at else None,
                'is_active': membership.is_active,
                'last_location_updated': membership.last_location_updated.isoformat() if membership.last_location_updated else None
            })
            groups_list.append(group_dict)
        
        return groups_list
        
    except ObjectDoesNotExist:
        raise Exception(f"User with ID {user_id} does not exist")
    except Exception as e:
        raise Exception(f"An error occurred while fetching user's groups: {str(e)}")

def get_my_active_group_list(user_id):

    try:
        user = User.objects.get(id=user_id)
        memberships = GroupMembership.objects.filter(user=user, is_active=True)
        groups_list = []
        for membership in memberships:
            group = membership.group
            group_dict = group.to_dict()
            
            # Add membership specific information
            group_dict.update({
                'is_admin': (group.admin_id == user_id),
                'joined_at': membership.joined_at.isoformat() if membership.joined_at else None,
                'last_location_updated': membership.last_location_updated.isoformat() if membership.last_location_updated else None
            })
            groups_list.append(group_dict)
        
        return groups_list
        
    except ObjectDoesNotExist:
        raise Exception(f"User with ID {user_id} does not exist")
    except Exception as e:
        raise Exception(f"An error occurred while fetching user's active groups: {str(e)}")


def create_group(admin_id,name, start_latitude, start_longitude, dest_latitude, dest_longitude, start_date, expected_end_date, joining_code, private=False):

    try:
        admin = User.objects.get(id=admin_id)
        group = Group(
            name=name,
            admin=admin,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            dest_latitude=dest_latitude,
            dest_longitude=dest_longitude,
            start_date=start_date,
            expected_end_date=expected_end_date,
            joining_code=joining_code,
            private=private,
            member_count=1,
        )
        group.save()
        group.members.add(admin)
        return group
    except ObjectDoesNotExist:
        raise Exception("Admin user does not exist")
    except Exception as e:
        raise Exception(f"An error occurred while creating the group: {str(e)}")
    


def leave_group(group_id, user_id):
    try:
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if group.admin.id == user.id:
            raise Exception("You cannot leave your own group")
        group.member_count -= 1
        group.save()
        group.members.remove(user)
        return group
    except ObjectDoesNotExist:
        raise Exception("Group or User does not exist")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    

def get_group_by_joining_code(group_id, user_id,joining_code):
    try:
        group = Group.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        if user in group.members.all():
            raise Exception("You are already a member of this group")

        if group.joining_code == joining_code:
            print ("Joining code is valid")
            group.members.add(user)
            group.member_count += 1
            group.save()
            return group
        else:
            raise Exception("Invalid joining code")
    except ObjectDoesNotExist:
        raise Exception("Group or User does not exist")