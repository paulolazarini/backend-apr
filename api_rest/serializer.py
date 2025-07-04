from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ArvorePreRequisitos, Objetivo, Obstaculo, PreRequisito, Dependencias

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False, allow_blank=False)
    first_name = serializers.CharField(required=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencias
        fields = ['id', 'requisito_origem', 'requisito_alvo']

class PreRequisitoSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = PreRequisito
        fields = ['id', 'nome_requisito', 'description', 'priority', 'priority_display']

class ObstaculoSerializer(serializers.ModelSerializer):
    pre_requisitos = PreRequisitoSerializer(many=True, read_only=True, source='prerequisito_set')

    class Meta:
        model = Obstaculo
        fields = ['id', 'nome_obstaculo', 'description', 'pre_requisitos']

class ObjetivoSerializer(serializers.ModelSerializer):
    obstaculos = ObstaculoSerializer(many=True, read_only=True, source='obstaculo_set')

    class Meta:
        model = Objetivo
        fields = ['id', 'nome_objetivo', 'description', 'obstaculos']

class ArvorePreRequisitosSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    objetivos = ObjetivoSerializer(many=True, read_only=True, source='objetivo_set')

    class Meta:
        model = ArvorePreRequisitos
        fields = ['id', 'nome_apr', 'description', 'user', 'user_id', 'objetivos']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)
        return super().update(instance, validated_data)