from rest_framework import serializers
from transactions.models.transaction_models import Transaction


class TransactionCreateSerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Transaction
        fields = (
            'uuid',
            'description',
            'category',
            'type',
            'value',
            'date',
            'account'
        )
        read_only_fields = ['uuid']

    def validate(self, attrs):
        attrs.pop('type', None)
        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj.category:
            return obj.category.category_type
        return None

    class Meta:
        model = Transaction
        fields = (
            'uuid',
            'description',
            'category',
            'type',
            'value',
            'date',
            'account'
        )
        read_only_fields = fields