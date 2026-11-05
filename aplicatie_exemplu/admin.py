from django.contrib import admin
from .models import Categorie, Brand, SpecificatieProdus, Produs, Contract

admin.site.register(Categorie)
admin.site.register(Brand)
admin.site.register(SpecificatieProdus)
admin.site.register(Produs)
admin.site.register(Contract)