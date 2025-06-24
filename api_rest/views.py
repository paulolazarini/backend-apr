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