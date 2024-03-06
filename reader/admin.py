from django.contrib import admin
from upload.models import UploadModel


# Register your models here.

class UploadModelAdmin(admin.ModelAdmin):
    list_display = ('File', "date", "obj")


admin.site.register(UploadModel, UploadModelAdmin)
