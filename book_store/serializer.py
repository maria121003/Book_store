from rest_framework import serializers
from .models import Genre, Book, Author, BookAuthor
from django.conf import settings

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        book = super().create(validated_data)
        if image:
            book.image_url = self.save_image(book, image)
            book.save()
        return book

    def save_image(self, book, image):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import os

        path = default_storage.save(os.path.join('images', str(book.id) + '_' + image.name), ContentFile(image.read()))
        return settings.MEDIA_URL + path

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = '__all__'        
