# Generated by Django 5.0.2 on 2024-03-08 21:52

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.FileField(upload_to='', validators=[core.validators.file_size], verbose_name='Файл')),
                ('obj', models.CharField(choices=[('kal', 'Калейдоскоп'), ('sun', 'Сан сити'), ('leo', 'Leomall'), ('stol', 'Столица')], default='Калейдоскоп', max_length=25, verbose_name='Объект')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
