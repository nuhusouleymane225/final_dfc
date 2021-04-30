from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import FeeReason, FeeRequest, UserProfile, Chauffeur
# Register your models here.
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import mark_safe
from django.template.defaultfilters import escape
from django.urls import reverse


class UserResource(resources.ModelResource):

    class Meta:
        model = UserProfile

class FeeRequestResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='Date', widget=widgets.DateWidget())
    id = fields.Field(attribute='id', column_name="Numéro d'édition")
    driver = fields.Field(attribute='driver', column_name='Chauffeur')
    activity = fields.Field(attribute='activity', column_name='Code frais')
    

    class Meta:
        model = FeeRequest
        fields = ('date', 'id', 'driver', 'activity')
        export_order = ('date', 'id', 'driver', 'activity')
        
         
    def dehydrate_user(self, FeeRequest):
        return '%s' % (FeeRequest.user.username)


    def dehydrate_driver(self, FeeRequest):
        return '%s' % (FeeRequest.driver.code_matricule)

   




class ChauffeurResource(resources.ModelResource):
    view_on_site = False
    class Meta:
        model = Chauffeur


class UserAdmin(ImportExportModelAdmin):
    view_on_site = False
    resource_class = UserResource

class FeeRequestAdmin(ImportExportModelAdmin):
    view_on_site = False
    list_filter = [
        'date',
        'validated',
        'user',
        'id',
        'level1',
        'level2'
        
        
    ]

    # permettre la recherche dans obj_repr et dans change_message

    search_fields = [
        
        'id',
      
    ]
    resource_class = FeeRequestResource


class ChauffeurAdmin(ImportExportModelAdmin):
    resource_class = ChauffeurResource




admin.site.register(Chauffeur, ChauffeurAdmin)
admin.site.register(FeeRequest, FeeRequestAdmin)
admin.site.register(UserProfile, UserAdmin)






@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    #pour avoir un deroulant basé sur l'heure
    date_hierarchy = 'action_time'

    #filtrer le resultat par utilisateur
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # permettre la recherche dans obj_repr et dans change_message

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
admin.site.site_header = "SUIVI DES FRAIS D'EXPLOITATION"


