from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели файлов.
    """

    file = serializers.FileField()
    uploaded_at = serializers.DateTimeField()
    processed = serializers.BooleanField()

    class Meta:
        model = File
        read_only_fields = ('id', 'uploaded_at', 'processed')
        fields = '__all__'
