from django.db import models


class File(models.Model):
    """
    Модель файла. Подразумевается, что сначала будет
    создан объект без файла, который будет добавлен позднее.
    """

    file = models.FileField(
        upload_to='files',
        null=True,
        blank=True,
        verbose_name="Файл"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    processed = models.BooleanField(
        default=False,
        verbose_name="Статус обработки"
    )
