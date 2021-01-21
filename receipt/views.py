from django.shortcuts import render
from .serializers import ReceiptSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Receipt

class ReceiptViewsets(ModelViewSet):
    serializer_class = ReceiptSerializer
    # queryset = Receipt.objects.all()


    def get_queryset(self):
        return Receipt.objects.filter(seller=self.request.user)

