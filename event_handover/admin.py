from django.contrib import admin
from django.contrib.admin import helpers

from .models import HandEvent, Comment
from .froms import CommentChangeForm, CommentAddForm

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from date_range_filter import DateRangeFilter


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
                    "handover_type", "publish_user", "recently_review",
                    "published_time", "status"]
    list_editable = ["status"]

    exclude = ['publish_user']
    inlines = [HandEventCommentInline]
    resource_class = HandEventResource

    change_readonly_fields = ["aircraft_code", "aircraft_type", "subject", "chapter_code",
                              "handover_type", "publish_user", "published_time"]

    list_filter = ["aircraft_code", "aircraft_type", "subject", "chapter_code",
                    "handover_type", "publish_user", ('published_time', DateRangeFilter), "status"]
    search_fields = ["aircraft_code", "aircraft_type", "subject", "chapter_code",
                     "handover_type"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.change_readonly_fields
        return []

    def get_queryset(self, request):
        from django.db.models import Max
        qs = super(HandEventAdmin, self).get_queryset(request)
        return qs.annotate(comment_time=Max("comment__created_at")).order_by("-comment_time")

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

    def recently_review(self, obj):
        comment = Comment.objects.filter(hand_event=obj).first()
        if comment:
            return comment.user.username + " " + \
                   comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "暂无回复"
    recently_review.short_description = "最新回复"
    # recently_review.admin_order_field = '-comment__created_at'

admin.site.register(HandEvent, HandEventAdmin)
