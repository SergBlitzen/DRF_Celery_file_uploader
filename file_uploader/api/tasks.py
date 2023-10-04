from pathlib import Path

from django.core import files
from django.core.files.storage import FileSystemStorage
from celery import shared_task

from files.models import File


@shared_task()
def handle_file(file_type, *args):

    # Простейший менеджер для обработки.
    if file_type == 'text':
        process_text.delay(*args)
    elif file_type == 'image':
        process_image(*args)
    elif file_type == 'audio':
        process_audio(*args)
    elif file_type == 'video':
        process_video(*args)
    elif file_type == 'application':
        process_application(*args)
    else:
        process_other_file_type(*args)


@shared_task()
def process_image(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)


@shared_task()
def process_text(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)


@shared_task()
def process_audio(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)


@shared_task()
def process_video(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)


@shared_task()
def process_application(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)


@shared_task()
def process_other_file_type(instance_id, path, file_name):
    storage = FileSystemStorage()
    path_object = Path(path)

    instance = File.objects.get(pk=instance_id)
    instance.processed = True

    with path_object.open(mode='rb') as f:
        file = files.File(f, name=path_object.name)
        instance = File.objects.get(pk=instance_id)
        instance.file = file
        instance.processed = True
        instance.save()

    storage.delete(file_name)