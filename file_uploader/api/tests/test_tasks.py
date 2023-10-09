import time

from django.core import files
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from files.models import File
from api.tasks import handle_file


class TaskTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_file = SimpleUploadedFile("test_file.txt", b"test_content")

    def test_file_handling(self):
        """
        Проверка создания и выполнения задания.
        """

        new_instance = File.objects.create()
        new_instance_id = new_instance.pk

        file = TaskTestCase.test_file
        file_type = file.content_type.split('/')[0]

        temp_storage = FileSystemStorage()
        temp_storage.save(file.name, files.File(file))

        self.task = handle_file.delay(
            file_type, new_instance_id, temp_storage.path(file.name), file.name
        )
        time.sleep(1)
        self.assertEqual(self.task.state, 'SUCCESS')
