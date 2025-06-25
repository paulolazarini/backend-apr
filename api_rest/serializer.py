from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ArvorePreRequisitos, Objetivo, Obstaculo, PreRequisito, Dependencias

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencias
        fields = ['id', 'requisito_origem', 'requisito_alvo']

class PreRequisitoSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    obstaculo_id = serializers.IntegerField(write_only=True, required=False)  # Opcional para edição
    
    class Meta:
        model = PreRequisito
        fields = ['id', 'nome_requisito', 'description', 'priority', 'priority_display', 'obstaculo_id']
    
    def create(self, validated_data):
        obstaculo_id = validated_data.pop('obstaculo_id')
        validated_data['obstaculo_id'] = obstaculo_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Remove obstaculo_id se presente (não deve mudar na edição)
        validated_data.pop('obstaculo_id', None)
        return super().update(instance, validated_data)

class ObstaculoSerializer(serializers.ModelSerializer):
    pre_requisitos = PreRequisitoSerializer(many=True, read_only=True, source='prerequisito_set')
    objetivo_id = serializers.IntegerField(write_only=True, required=False)  # Opcional para edição

    class Meta:
        model = Obstaculo
        fields = ['id', 'nome_obstaculo', 'description', 'pre_requisitos', 'objetivo_id']
    
    def create(self, validated_data):
        objetivo_id = validated_data.pop('objetivo_id')
        validated_data['objetivo_id'] = objetivo_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Remove objetivo_id se presente (não deve mudar na edição)
        validated_data.pop('objetivo_id', None)
        return super().update(instance, validated_data)

class ObjetivoSerializer(serializers.ModelSerializer):
    obstaculos = ObstaculoSerializer(many=True, read_only=True, source='obstaculo_set')
    arvore_id = serializers.IntegerField(write_only=True, required=False)  # Opcional para edição

    class Meta:
        model = Objetivo
        fields = ['id', 'nome_objetivo', 'description', 'obstaculos', 'arvore_id']
    
    def create(self, validated_data):
        arvore_id = validated_data.pop('arvore_id')
        validated_data['arvore_id'] = arvore_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Remove arvore_id se presente (não deve mudar na edição)
        validated_data.pop('arvore_id', None)
        return super().update(instance, validated_data)

class ArvorePreRequisitosSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)  # Opcional para edição
    objetivos = ObjetivoSerializer(many=True, read_only=True, source='objetivo_set')

    class Meta:
        model = ArvorePreRequisitos
        fields = ['id', 'nome_apr', 'description', 'user', 'user_id', 'objetivos']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        validated_data['user_id'] = user_id
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Remove user_id se presente (não deve mudar na edição)
        validated_data.pop('user_id', None)
        return super().update(instance, validated_data)