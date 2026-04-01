from django.contrib import admin

from RCPIEAPP.models import DepartmentDRC, Faculty, OtherDepartmentDRCHead, RCConvener, ResearchProposal, UserProfile

# Register your models here.

from django.contrib import admin
from .models import DRC_Member, DeanResearch, PublishedPaper, UserProfile, RCConvener, DepartmentDRC, OtherDepartmentDRCHead

@admin.action(description='Approve selected users')
def approve_users(modeladmin, request, queryset):
    for user_profile in queryset:
        if not user_profile.is_approved_by_admin:
            user_profile.is_approved_by_admin = True
            user_profile.save()

            if user_profile.role == 'RC Convener':
                RCConvener.objects.create(user_profile=user_profile)
            elif user_profile.role == 'Department DRC':
                DepartmentDRC.objects.create(user_profile=user_profile)
            elif user_profile.role == 'Other Department DRC Head':
                OtherDepartmentDRCHead.objects.create(user_profile=user_profile)
            elif user_profile.role == 'Research_Dean':
                DeanResearch.objects.create(user_profile=user_profile)
            elif user_profile.role == 'DRC_Member':
                DRC_Member.objects.create(user_profile=user_profile)
            user_profile.user.is_active = True
            user_profile.user.save()

admin.site.register(UserProfile, list_display=['user', 'role', 'is_approved_by_admin'], actions=[approve_users])

#admin.site.register(UserProfile)
admin.site.register(Faculty)
admin.site.register(RCConvener)
admin.site.register(DepartmentDRC)
admin.site.register(OtherDepartmentDRCHead)
admin.site.register(ResearchProposal)
admin.site.register(PublishedPaper)

