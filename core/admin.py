from django.contrib import admin
from .models import ItemCardapio, Comanda, ItemComanda


class ItemComandaInline(admin.TabularInline):
    model = ItemComanda
    extra = 1


@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cliente', 'status', 'criado_em', 'total')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome', 'cliente__nome_completo', 'id')
    inlines = [ItemComandaInline]


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'disponivel')
    list_filter = ('disponivel',)
    search_fields = ('nome',)


@admin.register(ItemComanda)
class ItemComandaAdmin(admin.ModelAdmin):
    list_display = ('comanda', 'item', 'quantidade', 'subtotal')
