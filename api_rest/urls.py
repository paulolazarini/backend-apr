from django.urls import path
from .views import (
    get_users, create_users, user_detail,
    apr_list, apr_detail,
    objetivo_list, objetivo_detail,
    obstaculo_list, obstaculo_detail,
    prerequisito_list, prerequisito_detail,
    dependencia_list, dependencia_detail,
    test_endpoint
)

urlpatterns = [
    path('test/', test_endpoint, name='test_endpoint'),
    # User endpoints
    path('users/', get_users, name='get_users'),
    path('users/create', create_users, name='create_users'),
    path('users/<int:id>', user_detail, name='user_detail'),
    
    # APR endpoints
    path('apr/', apr_list, name='apr_list'),
    path('apr/<int:id>', apr_detail, name='apr_detail'),
    
    # Objetivo endpoints
    path('apr/<int:apr_id>/objetivos/', objetivo_list, name='objetivo_list'),
    path('apr/<int:apr_id>/objetivos/<int:objetivo_id>', objetivo_detail, name='objetivo_detail'),
    
    # Obstáculo endpoints
    path('objetivos/<int:objetivo_id>/obstaculos/', obstaculo_list, name='obstaculo_list'),
    path('objetivos/<int:objetivo_id>/obstaculos/<int:obstaculo_id>', obstaculo_detail, name='obstaculo_detail'),
    
    # Pré-requisito endpoints
    path('obstaculos/<int:obstaculo_id>/prerequisitos/', prerequisito_list, name='prerequisito_list'),
    path('obstaculos/<int:obstaculo_id>/prerequisitos/<int:prerequisito_id>', prerequisito_detail, name='prerequisito_detail'),
    
    # Dependências endpoints
    path('dependencias/', dependencia_list, name='dependencia_list'),
    path('dependencias/<int:id>', dependencia_detail, name='dependencia_detail'),
]