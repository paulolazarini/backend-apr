from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    ArvorePreRequisitos,
    Objetivo,
    Obstaculo,
    PreRequisito,
    Dependencias
)
from .serializer import (
    UserSerializer,
    ArvorePreRequisitosSerializer,
    ObjetivoSerializer,
    ObstaculoSerializer,
    PreRequisitoSerializer,
    DependenciaSerializer
)

@api_view(['GET'])
def test_endpoint(request):
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response({
            'message': 'API is working',
            'database': 'connected'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'message': 'API is working but database error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def test_create_apr(request):
    try:
        # Testa criação simples
        from .models import ArvorePreRequisitos
        from django.contrib.auth.models import User
        
        user = User.objects.get(id=request.data.get('user_id', 2))
        apr = ArvorePreRequisitos.objects.create(
            nome_apr=request.data.get('nome_apr', 'Teste'),
            description=request.data.get('description', ''),
            user=user
        )
        
        return Response({
            'success': True,
            'id': apr.id,
            'nome_apr': apr.nome_apr
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def test_create_obstaculo(request):
    try:
        from .models import Obstaculo, Objetivo
        
        objetivo = Objetivo.objects.get(id=request.data.get('objetivo_id', 2))
        obstaculo = Obstaculo.objects.create(
            nome_obstaculo=request.data.get('nome_obstaculo', 'Teste'),
            description=request.data.get('description', ''),
            objetivo=objetivo
        )
        
        return Response({
            'success': True,
            'id': obstaculo.id,
            'nome_obstaculo': obstaculo.nome_obstaculo
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def test_create_prerequisito(request):
    try:
        from .models import PreRequisito, Obstaculo
        
        obstaculo = Obstaculo.objects.get(id=request.data.get('obstaculo_id', 1))
        prerequisito = PreRequisito.objects.create(
            nome_requisito=request.data.get('nome_requisito', 'Teste'),
            description=request.data.get('description', ''),
            priority=request.data.get('priority', 1),
            obstaculo=obstaculo
        )
        
        return Response({
            'success': True,
            'id': prerequisito.id,
            'nome_requisito': prerequisito.nome_requisito
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def test_create_dependencia(request):
    try:
        from .models import Dependencias, PreRequisito
        
        requisito_origem = PreRequisito.objects.get(id=request.data.get('requisito_origem', 1))
        requisito_alvo = PreRequisito.objects.get(id=request.data.get('requisito_alvo', 2))
        
        dependencia = Dependencias.objects.create(
            requisito_origem=requisito_origem,
            requisito_alvo=requisito_alvo
        )
        
        return Response({
            'success': True,
            'id': dependencia.id,
            'origem': requisito_origem.nome_requisito,
            'alvo': requisito_alvo.nome_requisito
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User views
@api_view(['GET'])
def get_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_users(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':    
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# APR views
@api_view(['GET', 'POST'])
def apr_list(request):
    if request.method == 'GET':
        arvores = ArvorePreRequisitos.objects.all()
        serializer = ArvorePreRequisitosSerializer(arvores, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArvorePreRequisitosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def apr_detail(request, id):
    try:
        arvore = ArvorePreRequisitos.objects.get(id=id)
    except ArvorePreRequisitos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ArvorePreRequisitosSerializer(arvore)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArvorePreRequisitosSerializer(arvore, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        arvore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Objetivo views
@api_view(['GET', 'POST'])
def objetivo_list(request, apr_id):
    try:
        arvore = ArvorePreRequisitos.objects.get(id=apr_id)
    except ArvorePreRequisitos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        objetivos = Objetivo.objects.filter(arvore=arvore)
        serializer = ObjetivoSerializer(objetivos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['arvore'] = apr_id
        serializer = ObjetivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def objetivo_detail(request, apr_id, objetivo_id):
    try:
        objetivo = Objetivo.objects.get(id=objetivo_id, arvore_id=apr_id)
    except Objetivo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ObjetivoSerializer(objetivo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ObjetivoSerializer(objetivo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        objetivo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Obstáculo views
@api_view(['GET', 'POST'])
def obstaculo_list(request, objetivo_id):
    try:
        objetivo = Objetivo.objects.get(id=objetivo_id)
    except Objetivo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        obstaculos = Obstaculo.objects.filter(objetivo=objetivo)
        serializer = ObstaculoSerializer(obstaculos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['objetivo'] = objetivo_id
        serializer = ObstaculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def obstaculo_detail(request, objetivo_id, obstaculo_id):
    try:
        obstaculo = Obstaculo.objects.get(id=obstaculo_id, objetivo_id=objetivo_id)
    except Obstaculo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ObstaculoSerializer(obstaculo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ObstaculoSerializer(obstaculo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        obstaculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Pré-requisito views
@api_view(['GET', 'POST'])
def prerequisito_list(request, obstaculo_id):
    try:
        obstaculo = Obstaculo.objects.get(id=obstaculo_id)
    except Obstaculo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        prerequisitos = PreRequisito.objects.filter(obstaculo=obstaculo)
        serializer = PreRequisitoSerializer(prerequisitos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['obstaculo'] = obstaculo_id
        serializer = PreRequisitoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def prerequisito_detail(request, obstaculo_id, prerequisito_id):
    try:
        prerequisito = PreRequisito.objects.get(id=prerequisito_id, obstaculo_id=obstaculo_id)
    except PreRequisito.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PreRequisitoSerializer(prerequisito)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PreRequisitoSerializer(prerequisito, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        prerequisito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Dependências views
@api_view(['GET', 'POST'])
def dependencia_list(request):
    if request.method == 'GET':
        dependencias = Dependencias.objects.all()
        serializer = DependenciaSerializer(dependencias, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DependenciaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def dependencia_detail(request, id):
    try:
        dependencia = Dependencias.objects.get(id=id)
    except Dependencias.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DependenciaSerializer(dependencia)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DependenciaSerializer(dependencia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        dependencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)