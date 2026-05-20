from typing import Any

from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data: Any, initial: Any | None = None) -> Any:
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]
        return [super(MultipleFileField, self).clean(data, initial)]

class CustomUploadWidget(MultipleFileInput):
    template_name = "upload_file/upload.html"

    def get_context(self, name: str, value: Any, attrs: dict[str, Any] | None) -> dict[str, Any]:
        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["object_id"] = attrs.get("object_id", "")
        ctx["widget"]["model_name"] = attrs.get("model_name", "")
        return ctx