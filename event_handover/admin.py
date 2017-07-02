from django.contrib import admin
from django.contrib.admin import helpers

from .models import HandEvent, Comment
from .froms import CommentChangeForm, CommentAddForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class HandEventResource(resources.ModelResource):

    class Meta:
        model = HandEvent


class HandEventCommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    exclude = ["user"]
    form = CommentChangeForm


class HandEventAdmin(ImportExportModelAdmin):
    list_display = ["aircraft_code", "aircraft_type", "subject", "chapter_code",
                    "handover_type", "publish_user", "published_time", "status"]
    list_editable = ["status"]

    exclude = ['publish_user']
    inlines = [HandEventCommentInline]
    resource_class = HandEventResource

    change_readonly_fields = ["aircraft_code", "aircraft_type", "subject", "chapter_code",
                              "handover_type", "publish_user", "published_time"]

    list_filter = list_display
    search_fields = list_display

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.change_readonly_fields
        return []

    def save_model(self, request, obj, form, change):
        if not change:
            obj.publish_user = request.user

        return super(HandEventAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets, prepopulated, readonly,
                model_admin=self,
            )
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets

admin.site.register(HandEvent, HandEventAdmin)