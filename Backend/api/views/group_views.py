from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..services import group_service
from ..serializers.group_serializer import GroupSerializer
import random
import json


'''
    # Esle sabbai group ko list dinxa listed nearest to fartheset-----------------------------------------------------------------------'''
@api_view(['GET','POST'])
def get_group_list(request):     
    if request.method == 'POST':
        try:
            longitude = request.decrypted_data.get('longitude')
            latitude = request.decrypted_data.get('latitude')
            list_of_group = group_service.getCompleteListGroups(longitude = longitude, latitude = latitude)
            serializer = GroupSerializer(list_of_group, many=True)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Invalid request method"}, status=405)
    return Response({"message": "Group list retrieved successfully","data" : serializer.data}, status=200)

'''
    # Esle sabai group haru ko list dinxa jun group ma user le join gareko xa'''

@api_view(['GET','POST'])
def get_my_group_list(request):   
    if request.method == 'POST':
        try:
            user_id = request.decrypted_data.get('user_id')
            list_of_group = group_service.getMyGroupList(user_id)
            serializer = GroupSerializer(list_of_group, many=True)
            return Response({"message": "My group list retrieved successfully", "data": serializer.data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

'''
    # Esle tyo user part bhako group haru dinxa only active group -----------------------------------------------------------
'''      
@api_view(['GET','POST'])
def get_my_active_group_list(request):  
    if request.method == 'POST':
        try:
            user_id = request.decrypted_data.get('user_id')
            list_of_group = group_service.get_my_active_group_list(user_id)
            serializer = GroupSerializer(list_of_group, many=True)
            return Response({"message": "My active group list retrieved successfully", "data": serializer.data}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
'''
  # Esle group ma join garna ko lagi ho -----------------------------------------------------------------------
'''
@api_view(['GET','POST'])
def join_group(request):  
    if request.method == 'POST':
        
        try:
            user_id = request.decrypted_data.get('user_id')
            group_id = request.decrypted_data.get('group_id')
            group_service.join_group( group_id,user_id)
            return Response({"message": "Successfully joined the group"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Invalid request method"}, status=405)
    
'''

leave group ko lagi ho -----------------------------------------------------------------------'''

@api_view(['GET','POST'])
def leave_group(request):  
    if request.method == 'POST':
        try:
            user_id = request.decrypted_data.get('user_id')
            group_id = request.decrypted_data.get('group_id')
            group_service.leave_group( group_id,user_id)
            return Response({"message": "Successfully left the group"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Invalid request method"}, status=405)

'''
Yo create group ko lagi ho -----------------------------------------------------------------------
'''
@api_view(['GET','POST'])
def create_group(request):  
    if request.method == 'POST':
        try:
            user_id = request.decrypted_data.get('user_id')
            group_name = request.decrypted_data.get('group_name')
            start_latitude = request.decrypted_data.get('start_latitude')
            start_longitude = request.decrypted_data.get('start_longitude')
            dest_latitude = request.decrypted_data.get('dest_latitude')
            dest_longitude = request.decrypted_data.get('dest_longitude')
            start_date = request.decrypted_data.get('start_date')
            expected_end_date = request.decrypted_data.get('expected_end_date')
            joining_code = random.randint(100000, 999999)  # Generate a random joining code
            private = request.decrypted_data.get('private', False)  # Default to False if not provided
            
            group_service.create_group(user_id, group_name, start_latitude, start_longitude, dest_latitude, dest_longitude, start_date, expected_end_date,joining_code, private)
            
            return Response({"message": "Group created successfully","share_code" : joining_code}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Invalid request method"}, status=405)


'''
Esle jun group private hunxa tesma join garna ko laagi code chahinxa ani tyo maatra handle gaarxa 
'''
@api_view(['GET','POST'])
def join_group_with_code(request):  
    if request.method == 'POST':
        try:
            user_id = request.decrypted_data.get('user_id')
            group_id = request.decrypted_data.get('group_id')
            joining_code = request.decrypted_data.get('joining_code')
            group_service.get_group_by_joining_code( group_id,user_id,joining_code)
            return Response({"message": "Successfully joined the group"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    else:
        return Response({"error": "Invalid request method"}, status=405)