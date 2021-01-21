from django.shortcuts import render
from .serializers import ReceiptSerializer
from rest_framework.viewsets import ModelViewSet


class ReceiptViewsets(ModelViewSet):
    serializer_class = ReceiptSerializer

