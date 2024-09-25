from django.contrib import admin

from .models import ListaItems, Revisiones


@admin.register(ListaItems)
class ListaItemsAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "familia", "revision", "g_x", "g_y", "y_x", "y_y", "r_x", "r_y")


@admin.register(Revisiones)
class RevisionesAdmin(admin.ModelAdmin):
    pass
