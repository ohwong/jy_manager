from functools import partial, reduce, update_wrapper

from django.contrib import admin
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.forms import model_to_dict

from django.http import HttpResponse
from wsgiref.util import FileWrapper
import weasyprint
from io import BytesIO

from .models import MCC, MccEquipment


class MccEquipmentAdmin(admin.TabularInline):

    model = MccEquipment
    extra = 1
    max_num = 15


class MCCAdmin(admin.ModelAdmin):

    search_fields = []

    list_display = ['order', 'aircraft', 'terminal', 'date']

    suit_form_tabs = (('base', '基本信息'), ('equipment', '航材与工装设备信'), ('feedback', '工作反馈'))
    inlines = [MccEquipmentAdmin]
    exclude = ['author']
    fieldsets = (


        ("基本信息", {
            'classes': ('suit-tab suit-tab-base',),
            'fields': ('order', 'aircraft', 'terminal', 'date', 'discrepancy_or_reason',
                       'work_content')
        }),
        ('计划工时', {
            'classes': ('suit-tab suit-tab-equipment',),
            'fields': ('plan_nam_hours', 'is_rll',
                       'is_run_test', 'reference', 'verifier'),
        }),
        ('工作反馈', {
            'classes': ('suit-tab suit-tab-feedback',),
            'fields': ('feedback_content',  'actual_nam_hours',  'worker', 'inspector',
                       "feed_back_date"),
        }),

    )

    def format_bool(self, value):
        if value is True:
            return "是"
        elif value is False:
            return "否"
        return value

    def pdf_view(self, request, object_id, extra_context=None):
        from django.template import Context, Template
        obj = MCC.objects.get(pk=object_id)
        c = model_to_dict(obj, exclude=['worker', 'inspector', 'verifier', 'author'])
        for k, v in c.items():
            c[k] = self.format_bool(v)

        c['worker'] = obj.worker.username if obj.worker else ''
        c['inspector'] = obj.inspector.username if obj.inspector else ''
        c['verifier'] = obj.verifier.username if obj.verifier else ''
        c['author'] = obj.author.username if obj.author else ''
        c['aircraft_code'] = obj.aircraft.aircraft_code if obj.aircraft else ''

        equipments = MccEquipment.objects.filter(mcc=obj)
        c.update({"equipments": equipments})
        response = TemplateResponse(
            request, 'mcc/mcc.html', c
        )
        # return response
        rendered_content = response.rendered_content

        pdf = weasyprint.HTML(string=rendered_content).write_pdf()

        buffer = BytesIO(pdf)
        response = HttpResponse(FileWrapper(buffer), content_type='application/pdf')
        return response

    def get_urls(self):
        from django.conf.urls import url
        urlpatterns = super(MCCAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urlpatterns = [url(r'^(.+)/pdf/$', wrap(self.pdf_view), name='%s_%s_pdf' % info)] + urlpatterns
        return urlpatterns

    def save_model(self, request, obj, form, change):

        if not change:
            obj.author = request.user
        return super(MCCAdmin, self).save_model(request, obj, form, change)


admin.site.register(MCC, MCCAdmin)
