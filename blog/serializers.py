from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'titulo', 'contenido', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']

    def validate_titulo(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value
    
    def validate_contenido(self, value):
        if not value:
            raise serializers.ValidationError("El contenido no puede estar vacío.")
        return value