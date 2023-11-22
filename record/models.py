from django.db import models
from Recording_project.settings import AUTH_USER_MODEL
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import F, Q

from record.validators import phone_validator, image_validator


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email',
                              unique=True,
                              error_messages={
                                  "unique": "такой email адрес уже зарегистрирован"}
                              )


class AbstractInfo(models.Model):
    """Передает общую информацию"""

    phone_number = models.CharField(verbose_name='Номер телефона',
                                    max_length=20,
                                    unique=True,
                                    blank=True,
                                    null=True,
                                    validators=[phone_validator],
                                    error_messages={
                                        'unique': 'такой номер телефона уже зарегистрирован'})

    date_joined = models.DateTimeField(verbose_name='Присоединился',
                                       default=timezone.now)

    class Meta:
        abstract = True


class Customers(AbstractInfo):

    user = models.OneToOneField(AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='customers')

    birth_date = models.DateField(verbose_name='Дата рождения',
                                  blank=True,
                                  null=True)

    photo = models.ImageField(verbose_name='Фото',
                              upload_to='photo_customer/',
                              validators=[image_validator],
                              blank=True,
                              default='default_photo/')

    class Meta:
        db_table = 'customers'


class Organizations(AbstractInfo):

    user = models.OneToOneField(AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='organizations')

    name = models.CharField(verbose_name='Название',
                            max_length=255)

    category = models.ForeignKey('categories',
                                 verbose_name='Категория',
                                 on_delete=models.SET_NULL,
                                 related_name='organizations',
                                 null=True)

    photo = models.ImageField(verbose_name='Фото',
                              upload_to='photo_organization/',
                              validators=[image_validator],
                              blank=True,
                              default='default_photo/')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'organizations'


class CategoriesChoices(models.TextChoices):
    SPORT = "sport", "спорт"
    TOURISM = "tourism", "туризм"
    EDUCATION = "education", "образование"
    SCIENCE = "science", "наука"
    ENTERTAINMENT = "entertainment", "развлечение"
    SUNDRY = "sundry", "разное"


class Categories(models.Model):
    name = models.CharField(max_length=50,
                            choices=CategoriesChoices.choices)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'categories'
        constraints = [
            models.CheckConstraint(check=Q(name__in=CategoriesChoices.values),
                                   name=f"check_{db_table}")
        ]


class Employees(AbstractInfo):

    organization = models.ForeignKey('organizations',
                                     on_delete=models.CASCADE,
                                     related_name='employees')

    firstname = models.CharField(verbose_name='Имя',
                                 max_length=255)

    lastname = models.CharField(verbose_name='Фамилия',
                                max_length=255)

    email = models.EmailField(verbose_name='Email',
                              unique=True,
                              error_messages={
                                  "unique": "такой email адрес уже зарегистрирован"})

    photo = models.ImageField(verbose_name='Фото',
                              upload_to='photo_employee/',
                              validators=[image_validator],
                              default='default_photo/',
                              blank=True)

    def __str__(self):
        return f"{self.firstname}"

    class Meta:
        db_table = 'employees'


class PaymentTariffChoices(models.TextChoices):
    PAID = "paid", "платный"
    FREE = "free", "бесплатный"


class StatusOpeningChoices(models.TextChoices):
    OPEN = "open", "открытый"
    CLOSED = "close", "закрытый"


class Events(models.Model):

    organization = models.ForeignKey('organizations',
                                     on_delete=models.CASCADE,
                                     related_name='events')

    employee = models.ManyToManyField('employees',
                                      verbose_name='Сотрудники',
                                      related_name='events')

    name = models.CharField(verbose_name='Название',
                            max_length=255)

    date_event = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Начало')
    end_time = models.TimeField(verbose_name='Конец')

    status_tariff = models.CharField(verbose_name='Статус',
                                     max_length=4,
                                     choices=PaymentTariffChoices.choices)

    status_opening = models.CharField(verbose_name='Вход',
                                      max_length=10,
                                      choices=StatusOpeningChoices.choices,
                                      default=StatusOpeningChoices.OPEN)

    limit_clients = models.SmallIntegerField(verbose_name='Лимит клиентов')
    quantity_clients = models.SmallIntegerField(verbose_name='Количество клиентов',
                                                default=0)

    price_event = models.DecimalField(verbose_name='Цена',
                                      max_digits=10,
                                      decimal_places=2,
                                      blank=True,
                                      null=True)

    description = models.TextField(verbose_name='Описание',
                                   blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'events'
        constraints = [
            models.CheckConstraint(check=Q(quantity_clients__lte=F("limit_clients")),
                                   name=f"check_quantity_clients_{db_table}"),
            models.CheckConstraint(check=Q(limit_clients__gt=0),
                                   name=f"check_limit_clients_{db_table}"),
            models.CheckConstraint(check=Q(status_tariff__in=PaymentTariffChoices.values),
                                   name=f"check_status_tariff_{db_table}"),
            models.CheckConstraint(check=Q(status_opening__in=StatusOpeningChoices.values),
                                   name=f"check_status_opening_{db_table}"),
            models.CheckConstraint(check=Q(start_time__lt=F("end_time")),
                                   name=f"check_time_{db_table}"),
        ]


class Recordings(models.Model):

    event = models.ForeignKey('events',
                              on_delete=models.CASCADE,
                              related_name='recordings')
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='recordings')

    class Meta:
        db_table = 'recordings'
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'],
                                    name=f"unique_{db_table}_user")
        ]


