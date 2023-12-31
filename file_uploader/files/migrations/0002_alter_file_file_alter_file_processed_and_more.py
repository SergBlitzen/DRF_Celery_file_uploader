# Generated by Django 4.2.5 on 2023-10-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='file',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='Статус обработки'),
        ),
        migrations.AlterField(
            model_name='file',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
    ]
