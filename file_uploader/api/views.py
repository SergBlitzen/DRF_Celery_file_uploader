from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.core import files
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from files.models import File
from api.tasks import handle_file
from api.serializers import FileSerializer


class FileCreateView(generics.CreateAPIView):
    """
    Вью для эндпоинта 'upload/'. Принимает файл в запросе,
    сохраняет во временное хранилище, создаёт новый пустой
    объект класса и отправляет его primary key с путем ко
    временному сохраненному файлу в задачу.
    """

    def create(self, request, *args, **kwargs):
        # Первоначальная проверка нужна на случай, если придёт
        # запрос с пустым значением поля "file".
        try:
            req_files = self.request.FILES
            file = self.request.FILES['file']
            # По mime-типу файла определяется
            # задача, которая его обработает.
            file_type = file.content_type.split('/')[0]
            # Жесткое ограничение нескольких файлов в запросе.
            if len(req_files.getlist('file')) > 1:
                raise APIException("Можно отправить только 1 файл!")
            if settings.MAX_FILE_SIZE:
                max_size = settings.MAX_FILE_SIZE
                if len(file) > max_size:
                    # Приведение в мегабайты для более простого восприятия.
                    max_size_mb = max_size / 1024 / 1024
                    raise APIException(
                        f"Размер файла превышает допустимый! "
                        f"Максимальный объём файла: {max_size_mb} мб."
                    )
        except MultiValueDictKeyError:
            raise APIException("В запросе отсуствует файл!")

        instance = File.objects.create()
        instance_id = instance.pk
        temp_storage = FileSystemStorage()
        temp_storage.save(file.name, files.File(file))
        handle_file.delay(
            file_type, instance_id, temp_storage.path(file.name), file.name
        )
        serializer = FileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileListView(generics.ListAPIView):
    """
    View для вывода списка всех загруженных файлов.
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
