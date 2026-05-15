"""
Views for NetBox assets-management Plugin.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/
"""
import logging
from django.db import transaction, router
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from extras.models.models import ImageAttachment
from extras.ui.panels import TagsPanel
from netbox.views.generic.feature_views import ObjectImageAttachmentsView
from utilities.exceptions import AbortRequest, PermissionsViolation
from utilities.forms.utils import restrict_form_fields
from utilities.views import GetRelatedModelsMixin
from utilities.views import ViewTab, register_model_view
from netbox.views import generic
from netbox.ui import layout
from extras.ui.panels import ImageAttachmentsPanel
from django.contrib.contenttypes.models import ContentType
from .ui.panels import AssetPanel, AssetsGroupPanel
from django.shortcuts import redirect, render
from . import filtersets, forms, models, tables
from netbox.ui import panels
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .bulk_edit_forms import AssetBulkEditForm, AssetGroupBulkEditForm
from .bulk_import_forms import AssetCSVForm, AssetGroupCSVForm

def get_image_count(obj):
    try:
        # Use object_type_id to match NetBox's internal field schema
        return ImageAttachment.objects.filter(
            object_type_id=ContentType.objects.get_for_model(obj).id,
            object_id=obj.pk
        ).count()
    except Exception:
        return 0
    
class AssetGroupView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = models.AssetGroup.objects.all()
    
    layout = layout.SimpleLayout(
        left_panels=[
            # Panel thông tin cơ bản
            AssetsGroupPanel(),
            TagsPanel()
        ], 
        right_panels=[
            panels.RelatedObjectsPanel(),
            ImageAttachmentsPanel(),
        ]
    )
    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(
                request,
                instance,
                omit=[],
            )
        }
@register_model_view(model= models.AssetGroup, name="images", path="images")
class AssetGroupImageView(ObjectImageAttachmentsView):
    queryset= models.AssetGroup.objects.all()
    child_model= ImageAttachment
    template_name = 'generic/object_children.html'
    tab = ViewTab(
        label='Images',
        badge=get_image_count,
        weight=500
    )
    def get(self, request, *args, **kwargs):
        kwargs['model'] = models.AssetGroup
        return super().get(request, *args, **kwargs)
    
@register_model_view(model= models.Asset, name="images", path="images")
class AssetImageView(ObjectImageAttachmentsView):
    queryset= models.Asset.objects.all()
    child_model= ImageAttachment
    template_name = 'generic/object_children.html'
    tab = ViewTab(
        label='Images',
        badge=get_image_count,
        weight=500
    )
    def get(self, request, *args, **kwargs):
        kwargs['model'] = models.Asset
        return super().get(request, *args, **kwargs)
    
class AssetGroupListView(generic.ObjectListView):
    
    queryset = models.AssetGroup.objects.all()
    table = tables.AssetGroupTable
    filterset = filtersets.AssetGroupFilterSet
    filterset_form= forms.AssetGroupFilterForm

class AssetGroupCreateView(generic.ObjectEditView):
    queryset = models.AssetGroup.objects.all()
    form = forms.AssetGroupForm
    def alter_object(self, obj, request, url_args, url_kwargs):
        
        if obj.pk is None and not obj.created_by:
            obj.created_by = request.user
        return obj
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectEditView')
        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, 'snapshot'):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        form_prefix = 'quickadd' if request.GET.get('_quickadd') else None
        form = self.form(data=request.POST, files=request.FILES, instance=obj, prefix=form_prefix)
        restrict_form_fields(form, request.user)

        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop('changelog_message', '')

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

                
                    uploaded_file = request.FILES.get('attachment')
                    if uploaded_file:
                        try:
                            content_type = ContentType.objects.get_for_model(obj)
                            image = ImageAttachment(
                                object_type=content_type,
                                object_id=obj.pk,
                                name=uploaded_file.name.rsplit('.', 1)[0],
                        )
                            image.image.save(uploaded_file.name, uploaded_file, save=True)
                            messages.success(request, f"Uploaded File: {uploaded_file.name}")
                        except Exception as e:
                            raise ValidationError(f"Error while uploading file: {e}")

                
                msg = '{} {}'.format(
                    'Created' if object_created else 'Modified',
                    self.queryset.model._meta.verbose_name
                )
                logger.info(f"{msg} {obj} (PK: {obj.pk})")
                if hasattr(obj, 'get_absolute_url'):
                    msg = mark_safe(f'{msg} <a href="{obj.get_absolute_url()}">{escape(obj)}</a>')
                else:
                    msg = f'{msg} {obj}'
                messages.success(request, msg)

                
                if '_quickadd' in request.POST:
                    return render(request, 'htmx/quick_add_created.html', {
                        'object': obj,
                    })

                
                if '_addanother' in request.POST:
                    redirect_url = request.path
                    return redirect(redirect_url)

                return_url = self.get_return_url(request, obj)

                # HTMX
                if request.htmx:
                    from django.http import HttpResponse
                    return HttpResponse(headers={'HX-Location': return_url})

                return redirect(return_url)

            except (AbortRequest, PermissionsViolation) as e:
                logger.debug(e.message)
                form.add_error(None, e.message)

        else:
            logger.debug("Form validation failed")

        context = {
            'model': model,
            'object': obj,
            'form': form,
            'return_url': self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if '_quickadd' in request.POST:
            return render(request, 'htmx/quick_add.html', context)

        return render(request, self.template_name, context)
                
    


class AssetGroupEditView(generic.ObjectEditView):
    queryset = models.AssetGroup.objects.all()
    form = forms.AssetGroupEditForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        
        if obj.pk is None and not obj.created_by:
            obj.created_by = request.user
        return obj

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("netbox.views.ObjectEditView")

        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, "snapshot"):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        # Khởi tạo form
        form_prefix = "quickadd" if request.GET.get("_quickadd") else None
        form = self.form(
            data=request.POST,
            files=request.FILES,
            instance=obj,
            prefix=form_prefix,
        )
        restrict_form_fields(form, request.user)

        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop(
                "changelog_message", ""
            )

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

                    
                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

               
                    uploaded_file = request.FILES.get("attachment")
                    selected_image = form.cleaned_data.get("image_attachment")

                    if uploaded_file:
                        try:
                            if selected_image:
                                image = selected_image
                            else:
                                content_type = ContentType.objects.get_for_model(obj)
                                image = ImageAttachment(
                                    object_type=content_type,
                                    object_id=obj.pk,
                                )

                            image.name = uploaded_file.name.rsplit(".", 1)[0]

                            image.image.save(
                                uploaded_file.name,
                                uploaded_file,
                                save=True,
                            )

                            if selected_image:
                                messages.success(
                                    request,
                                    f"Updated File Success: {uploaded_file.name}"
                                )
                            else:
                                messages.success(
                                    request,
                                    f"Uploaded New File: {uploaded_file.name}"
                                )

                        except Exception as e:
                            raise ValidationError(f"Error while uploading file: {e}")

                
                msg = "{} {}".format(
                    "Created" if object_created else "Modified",
                    self.queryset.model._meta.verbose_name,
                )

                logger.info(f"{msg} {obj} (PK: {obj.pk})")

                if hasattr(obj, "get_absolute_url"):
                    msg = mark_safe(
                        f'<a href="{obj.get_absolute_url()}">{msg} {escape(obj)}</a>'
                    )
                else:
                    msg = f"{msg} {obj}"

                messages.success(request, msg)

                
                if "_quickadd" in request.POST:
                    return render(
                        request,
                        "htmx/quick_add_created.html",
                        {"object": obj},
                    )

                
                if "_addanother" in request.POST:
                    return redirect(request.path)

                
                return_url = self.get_return_url(request, obj)

                
                if request.htmx:
                    from django.http import HttpResponse

                    return HttpResponse(
                        headers={"HX-Location": return_url}
                    )

                return redirect(return_url)

            except (AbortRequest, PermissionsViolation, ValidationError) as e:
                error_message = getattr(e, "message", str(e))
                logger.debug(error_message)
                form.add_error(None, error_message)

        else:
            logger.debug("Form validation failed")

        # Render lại form nếu lỗi
        context = {
            "model": model,
            "object": obj,
            "form": form,
            "return_url": self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if "_quickadd" in request.POST:
            return render(request, "htmx/quick_add.html", context)

        return render(request, self.template_name, context)

        

class AssetGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.AssetGroup.objects.all()

    
class AssetGroupBulkEditView(generic.BulkEditView):
    queryset= models.AssetGroup.objects.all()
    filterset = filtersets.AssetGroupFilterSet
    table = tables.AssetGroupTable
    form = AssetGroupBulkEditForm

class AssetGroupBulkDeleteView(generic.BulkDeleteView):
    queryset= models.AssetGroup.objects.all()
    filterset = filtersets.AssetGroupFilterSet
    table = tables.AssetGroupTable

class AssetGroupBulkImportView(generic.BulkImportView):
    queryset= models.AssetGroup.objects.all()
    model_form= AssetGroupCSVForm
    table = tables.AssetGroupTable
    def save_object(self, object_form, request):
        obj = object_form.save(commit=False)
        if obj.pk is None and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        obj.save()
        object_form.save_m2m()
        return obj
    

@register_model_view(models.AssetGroup, name="assets")
class AssestGroupAssetsListView(generic.ObjectChildrenView):
    queryset= models.AssetGroup.objects.all()
    child_model= models.Asset
    table= tables.AssetTable
    
    tab= ViewTab(
        label="Assets",
        permission="assets_management_plugin.view_asset",
        weight=500,
        hide_if_empty=False,
        badge= lambda obj: obj.assets.count()
    )
    def get_children(self, request, parent):
        return parent.assets.all()
    
#Assets
class AssetListView(generic.ObjectListView):
    queryset= models.Asset.objects.all()
    table= tables.AssetTable    
    filterset= filtersets.AssetFilterSet
    filterset_form= forms.AssetFilterForm
    
class AssetView(GetRelatedModelsMixin,generic.ObjectView):
    queryset= models.Asset.objects.all()
    layout= layout.SimpleLayout(
        left_panels= [
            AssetPanel(),
            TagsPanel()
            
        ], 
        right_panels= [
            panels.RelatedObjectsPanel(),
            ImageAttachmentsPanel()
        ]
    )
    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(
                request,
                instance,
                omit=[],
            )
        }
    
class AssetCreateView(generic.ObjectEditView):
    queryset= models.Asset.objects.all()
    form= forms.AssetForm
    def alter_object(self, obj, request, url_args, url_kwargs):
        
        if obj.pk is None and not obj.created_by:
            obj.created_by = request.user
        
        if obj.purchase_date and obj.warranty_period_months:
            obj.warranty_expiration_date= obj.purchase_date + relativedelta(months=obj.warranty_period_months)
        return obj
    
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectEditView')
        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, 'snapshot'):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        form_prefix = 'quickadd' if request.GET.get('_quickadd') else None
        form = self.form(data=request.POST, files=request.FILES, instance=obj, prefix=form_prefix)
        restrict_form_fields(form, request.user)
        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop('changelog_message', '')

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

                
                    uploaded_file = request.FILES.get('attachment')
                    if uploaded_file:
                        try:
                            content_type = ContentType.objects.get_for_model(obj)
                            image = ImageAttachment(
                                object_type=content_type,
                                object_id=obj.pk,
                                name=uploaded_file.name.rsplit('.', 1)[0],
                            )
                            image.image.save(uploaded_file.name, uploaded_file, save=True)
                            messages.success(request, f"Uploaded: {uploaded_file.name}")
                        except Exception as e:
                            raise ValidationError(f"Error while uploading file: {e}")

                
                msg = '{} {}'.format(
                    'Created' if object_created else 'Modified',
                    self.queryset.model._meta.verbose_name
                )
                logger.info(f"{msg} {obj} (PK: {obj.pk})")
                if hasattr(obj, 'get_absolute_url'):
                    msg = mark_safe(f'{msg} <a href="{obj.get_absolute_url()}">{escape(obj)}</a>')
                else:
                    msg = f'{msg} {obj}'
                messages.success(request, msg)

                
                if '_quickadd' in request.POST:
                    return render(request, 'htmx/quick_add_created.html', {
                        'object': obj,
                    })

                
                if '_addanother' in request.POST:
                    redirect_url = request.path
                    return redirect(redirect_url)

                return_url = self.get_return_url(request, obj)

                # HTMX
                if request.htmx:
                    from django.http import HttpResponse
                    return HttpResponse(headers={'HX-Location': return_url})

                return redirect(return_url)

            except (AbortRequest, PermissionsViolation, ValidationError) as e:
                logger.debug(e.message)
                form.add_error(None, e.message)
            
        else:
            logger.debug("Form validation failed")

        context = {
            'model': model,
            'object': obj,
            'form': form,
            'return_url': self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if '_quickadd' in request.POST:
            return render(request, 'htmx/quick_add.html', context)

        return render(request, self.template_name, context)
        

class AssetEditView(generic.ObjectEditView):
    queryset = models.Asset.objects.all()
    form = forms.AssetEditForm
    def alter_object(self, obj, request, url_args, url_kwargs):
        
        if obj.pk is None and not obj.created_by:
            obj.created_by = request.user
        return obj
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("netbox.views.ObjectEditView")

        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, "snapshot"):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        # Khởi tạo form
        form_prefix = "quickadd" if request.GET.get("_quickadd") else None
        form = self.form(
            data=request.POST,
            files=request.FILES,
            instance=obj,
            prefix=form_prefix,
        )
        restrict_form_fields(form, request.user)

        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop(
                "changelog_message", ""
            )

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

                    uploaded_file = request.FILES.get("attachment")
                    selected_image = form.cleaned_data.get("image_attachment")

                    if uploaded_file:
                        try:
                            if selected_image:
                                image = selected_image
                                
                            else:
                                content_type = ContentType.objects.get_for_model(obj)
                                image = ImageAttachment(
                                    object_type=content_type,
                                    object_id=obj.pk,
                            )
                            image.name = uploaded_file.name.rsplit(".", 1)[0]
                            image.image.save(
                                uploaded_file.name,
                                uploaded_file,
                                save=True,
                            )
                            if selected_image:
                                messages.success(
                                request,
                                f"Updated Image Successfully: {uploaded_file.name}"
                            )
                            else:
                                messages.success(
                                request,
                                f"Upload new image successfully: {uploaded_file.name}"
                            )

                        except Exception as e:
                            raise ValidationError(f"Error while uploading file: {e}")

                
                msg = "{} {}".format(
                    "Created" if object_created else "Modified",
                    self.queryset.model._meta.verbose_name,
                )

                logger.info(f"{msg} {obj} (PK: {obj.pk})")

                if hasattr(obj, "get_absolute_url"):
                    msg = mark_safe(
                        f'<a href="{obj.get_absolute_url()}">{msg} {escape(obj)}</a>'
                    )
                else:
                    msg = f"{msg} {obj}"

                messages.success(request, msg)

                
                if "_quickadd" in request.POST:
                    return render(
                        request,
                        "htmx/quick_add_created.html",
                        {"object": obj},
                    )

                
                if "_addanother" in request.POST:
                    return redirect(request.path)

                
                return_url = self.get_return_url(request, obj)

                
                if request.htmx:
                    from django.http import HttpResponse

                    return HttpResponse(
                        headers={"HX-Location": return_url}
                    )

                return redirect(return_url)

            except (AbortRequest, PermissionsViolation, ValidationError) as e:
                error_message = getattr(e, "message", str(e))
                logger.debug(error_message)
                form.add_error(None, error_message)

        else:
            logger.debug("Form validation failed")

        # Render lại form nếu lỗi
        context = {
            "model": model,
            "object": obj,
            "form": form,
            "return_url": self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if "_quickadd" in request.POST:
            return render(request, "htmx/quick_add.html", context)

        return render(request, self.template_name, context)
    

class AssetDeleteView(generic.ObjectDeleteView):
    queryset = models.Asset.objects.all()
    
class AssetBulkEditView(generic.BulkEditView):
    queryset = models.Asset.objects.all()
    filterset = filtersets.AssetFilterSet
    table = tables.AssetTable
    form = AssetBulkEditForm

class AssetBulkDeleteView(generic.BulkDeleteView):
    queryset= models.Asset.objects.all()
    filterset= filtersets.AssetFilterSet
    table= tables.AssetTable

class AssetBulkImportView(generic.BulkImportView):
    queryset = models.Asset.objects.all()
    model_form = AssetCSVForm
    def save_object(self, object_form, request):
        obj = object_form.save(commit=False)
        if obj.pk is None and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        obj.save()
        object_form.save_m2m()
        return obj
    