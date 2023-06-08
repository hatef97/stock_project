from rest_framework import serializers


class BuyStockSerializer(serializers.Serializer):
    user = serializers.CharField()
    stockname = serializers.CharField()
    quantity = serializers.IntegerField()
