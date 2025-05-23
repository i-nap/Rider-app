from django.contrib import admin
from .models.group_model import  Group, GroupMembership
from .models.user_model import User
class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1
    fields = ('user', 'is_active', 'joined_at', 'last_location_updated')
    readonly_fields = ('joined_at',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'member_count', 'start_date', 'expected_end_date')
    search_fields = ('name', 'admin__full_name')
    list_filter = ('start_date', 'expected_end_date')
    inlines = [GroupMembershipInline]
    
    def get_queryset(self, request):
        # Prefetch related admin users to avoid N+1 queries
        return super().get_queryset(request).select_related('admin')

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'profile_photo_url')
        }),
        ('Authentication', {
            'fields': ('password_hash',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'joined_at', 'is_active')
    list_filter = ('is_active', 'joined_at')
    search_fields = ('user__full_name', 'group__name')
    raw_id_fields = ('user', 'group')

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)

admin.site.site_header = "Travel Group Admin"
admin.site.site_title = "Travel Group Admin Portal"
admin.site.index_title = "Welcome to Travel Group Admin Portal"