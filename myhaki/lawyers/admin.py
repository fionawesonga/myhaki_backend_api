# myhaki/lawyers/admin.py
from django.contrib import admin
from .models import User, Lawyer, CPDPoint, Case

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'role', 'first_name', 'last_name', 'is_deleted')
    list_filter = ('role', 'is_deleted')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('lawyer_id', 'user', 'practice_number', 'verified', 'created_at')
    list_filter = ('verified',)
    search_fields = ('practice_number', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CPDPoint)
class CPDPointAdmin(admin.ModelAdmin):
    list_display = ('cpd_id', 'lawyer', 'case', 'points_earned', 'created_at')
    list_filter = ('points_earned',)
    search_fields = ('lawyer__practice_number', 'case__case_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'created_at')
    readonly_fields = ('created_at', 'updated_at')