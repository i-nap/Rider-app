from django.urls import path
from ..views.group_views import get_group_list, get_my_group_list , get_my_active_group_list, join_group,create_group, leave_group,join_group_with_code
from django.http import JsonResponse
from ..views.auth_views import signup, verify_email,login

urlpatterns = [
    path('getGroupList/', get_group_list, name='get-group-list'),
    path('getMyGroupList/', get_my_group_list, name='get-group-list'),
    path('getMyActiveGroupList/', get_my_active_group_list, name='get-my-active-group-list'),
    path('joinGroup/', join_group, name='join-group'),
    path('createGroup/', create_group, name='create-group'),
    path('leaveGroup/', leave_group, name='leave-group'),
    path('joinPrivGroup/', join_group_with_code, name='join-private-group'),
    path('signup/', signup, name='signup'),
    path('signup/verify/', verify_email, name='verify-email'),
    path('login/',login, name='login'),

]
