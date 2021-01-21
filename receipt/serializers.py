from rest_framework import serializers
from .models import Item, Receipt



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'



class ReceiptSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)
    class Meta:
        model = Receipt
        fields = '__all__'


    def create(self, validated_data):
        validated_items = validated_data.pop('item')
        receipt_instance = Receipt.objects.create(**validated_data)
        for item in validated_items:
            created_item= Item.objects.create(**item)
            receipt_instance.item.add(created_item)
        return receipt_instance

