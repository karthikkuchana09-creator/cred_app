from django.contrib.auth.models import AbstractUser
from django.db import models


def mask_card_number(number: str):
    cleaned = ''.join(filter(str.isdigit, number))
    return '**** **** **** ' + cleaned[-4:]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    masked_number = models.CharField(max_length=19)
    last4 = models.CharField(max_length=4)
    card_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'last4')

    def save(self, *args, **kwargs):
        if not self.masked_number and self.last4:
            self.masked_number = '**** **** **** ' + self.last4
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('SUCCESS', 'SUCCESS'),
        ('FAILED', 'FAILED'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_logs')
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
