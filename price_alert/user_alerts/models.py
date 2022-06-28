from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAlert(models.Model):
    STATUS_CHOICES = (
        ("A", "ACTIVE"),
        ("D", "DEACTIVE"),
        ("T", "TRIGGERED")
    )
    ALERT_CHOICES= (
        ("G", "GREATER THAN"),
        ("GE", "GREATER THAN OR EQUAL"),
        ("E", "EQUAL"),
        ("L", "LESS THAN"),
        ("LE", "LESS THAN OR EQUAL"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default= "A" )
    alert_on = models.CharField(max_length=2, choices = ALERT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username