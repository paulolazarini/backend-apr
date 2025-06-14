from django.contrib import admin
from .models import (
    ArvorePreRequisitos,
    Objetivo,
    Obstaculo,
    PreRequisito,
    Dependencias
)

admin.site.register(ArvorePreRequisitos)
admin.site.register(Objetivo)
admin.site.register(Obstaculo)
admin.site.register(PreRequisito)
admin.site.register(Dependencias)

