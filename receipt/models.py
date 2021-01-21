from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Item(models.Model):
    name = models.CharField(max_length=500)
    desc = models.TextField()
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    unit_price = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.name


class Receipt(models.Model):
    buyer_name = models.CharField(max_length=500)
    buyer_address = models.CharField(max_length=500)
    buyer_email = models.EmailField(null=True, blank=True)
    buyer_phone_number = PhoneNumberField()
    issue_date = models.DateField()
    due_date = models.DateField()
    item = models.ManyToManyField(Item)
    notes = models.TextField()

    def __str__(self):
        return self.buyer_name

    def clean(self):
        if self.due_date < self.issue_date:
            raise ValidationError('Issue Date is ahead of Due Date')



