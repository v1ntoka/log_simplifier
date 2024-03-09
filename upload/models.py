from django.db import models
from core.validators import file_size


class UploadModel(models.Model):
    _choices = (
        ("kal", "Калейдоскоп"),
        ("sun", "Сан сити"),
        ("leo", "Leomall"),
        ("stol", "Столица")
    )
    File = models.FileField(
        upload_to='',
        validators=(file_size,),
        verbose_name="Файл",
    )
    obj = models.CharField(max_length=25, choices=_choices, default="Калейдоскоп", verbose_name="Объект")
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=225, default="jopa", primary_key=True)

    # def delete(self, *args, **kwargs):
    #     storage, path = self.File.storage, self.File.path
    #     storage.delete(path)
    #     super(UploadModel, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.name = f"{self.File.name}__{self.obj}"
        self.File.name = self.name
        super(UploadModel, self).save(*args, **kwargs)
