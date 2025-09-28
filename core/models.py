from django.db import models
from django.conf import settings


class ItemCardapio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Comanda(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_preparo', 'Em preparo'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    nome = models.CharField(
        max_length=100,
        help_text="Identificação da comanda (ex: Mesa 5, Delivery João, Pedido #123)"
    )
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comandas",
        blank=True,
        null=True,
        help_text="Cliente vinculado (opcional)"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberta'
    )

    def __str__(self):
        return f"{self.nome} - {self.get_status_display()}"

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())


class ItemComanda(models.Model):
    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE,
        related_name="itens"
    )
    item = models.ForeignKey(ItemCardapio, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} ({self.comanda.nome})"

    def subtotal(self):
        return self.item.preco * self.quantidade
