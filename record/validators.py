from django.core.validators import RegexValidator, FileExtensionValidator


class NumberValidator(RegexValidator):
    regex = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    code = 'invalid_number'
    message = 'Введите корректный номер телефона'


phone_validator = NumberValidator()

image_validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'],
                                         message='Загрузите корректный формат',
                                         code='invalid_image')


