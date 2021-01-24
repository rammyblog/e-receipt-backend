from rest_framework import serializers

from core.mixins.CustomErrorSerializer import CustomErrorSerializer
from .models import Item, Receipt



class ItemSerializer(CustomErrorSerializer,serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'



class ReceiptSerializer(CustomErrorSerializer,serializers.ModelSerializer):
    item = ItemSerializer(many=True)
    class Meta:
        model = Receipt
        fields = '__all__'


    def get_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        return user

    def create(self, validated_data):
        validated_items = validated_data.pop('item')
        validated_data["seller"] = self.get_user()

        receipt_instance = Receipt.objects.create(**validated_data)
        for item in validated_items:
            created_item= Item.objects.create(**item)
            receipt_instance.item.add(created_item)
        return receipt_instance

