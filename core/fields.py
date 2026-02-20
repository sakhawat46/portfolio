from django.db import models

try:
    from ckeditor.fields import RichTextField as CkeditorRichTextField
except Exception:
    CkeditorRichTextField = None


class RichTextField(models.TextField):
    """Fallback to TextField when CKEditor is not installed yet."""

    def __new__(cls, *args, **kwargs):
        if CkeditorRichTextField is not None:
            return CkeditorRichTextField(*args, **kwargs)
        return super().__new__(cls)
