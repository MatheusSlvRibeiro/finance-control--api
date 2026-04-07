from django.db import models
from core.mixins.models import BaseModel
from django.utils import timezone

class Transaction(BaseModel):
    description = models.CharField(
        max_length=100,
        verbose_name='Descrição',
        blank=False
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name='Categoria',
    )
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Valor'
    )
    date = models.DateTimeField(
        verbose_name='Data da transação',
        default=timezone.now
    )

    # Relacionamentos

    account = models.ForeignKey(
        'accounts.account',
        on_delete = models.CASCADE,
        null=False,
        blank=False,
        related_name='transactions',
        verbose_name='Conta'
    )


    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        permissions = [
            ('can_view_transaction', 'Can_view_transaction'),
            ('can_edit_transaction', 'Can_edit_transaction'),
            ('can_delete_transaction', 'Can_delete_transaction'),
        ]

    def __str__(self):
        return super().__str__()