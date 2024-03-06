from django.db import models
from core.validators import file_size


class UploadModel(models.Model):
    _choices = (zip((str(i) for i in range(100)), (
        "Калейдоскоп",
        "Сан сити",
        "Leomall",
        "Столица"
    )))
    File = models.FileField(
        upload_to='',
        validators=(file_size,),
        verbose_name="Файл",
    )
    obj = models.CharField(max_length=25, choices=_choices, default="Калейдоскоп", verbose_name="Объект")
    date = models.DateField(auto_now_add=True)
