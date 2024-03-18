from django import forms as f
from core.regex import Patterns
from django.core.validators import RegexValidator


class Filters(f.Form):
    date_before = f.DateTimeField(
        required=False,
        widget=f.DateTimeInput(
            attrs={
                "class": "form-control mb-2 mr-sm-2",
                "type": "datetime-local",
                'help_text': "Верхняя граница даты и времени"
            }
        )
    )
    date_after = f.DateTimeField(
        required=False,
        widget=f.DateTimeInput(
            attrs={
                "class": "form-control mb-2 mr-sm-2",
                "type": "datetime-local",
                "help_text": "Нижняя граница даты и времени",
            }
        ),
    )
    plate = f.CharField(
        required=False,
        widget=f.TextInput(
            attrs={
                "class": "form-control mb-2 mr-sm-2",
                "placeholder": "Номер автомобиля"
            }
        ),
        # Пока регулярка готова только для русских авто
        #     validators=[
        #         RegexValidator(Patterns.plate, message='Введите корректный номер')
        #     ]
    )
    entrance = f.CharField(
        required=False,
        widget=f.TextInput(
            attrs={
                "class": "form-control mb-2 mr-sm-2",
                "placeholder": "Выезд"
            }
        )
    )
    extra = f.CharField(
        required=False,
        widget=f.TextInput(
            attrs={
                "class": "form-control mb-2 mr-sm-2",
                "placeholder": "Дополнительно"
            }
        )
    )

    # def is_valid(self):
    #     old = super().is_valid()
    #     new = old
    #     if new and self.plate:
    #         if not (re.match(Patterns.plate, self.plate) or self.plate == ''):
    #             new = False
    #     if new and self.exit:
    #         if not (re.match(Patterns.exit, self.exit) or self.exit == ''):
    #             new = False
    #     return new and old
