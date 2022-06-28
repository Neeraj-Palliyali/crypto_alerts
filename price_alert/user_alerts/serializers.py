from rest_framework import serializers
from user_alerts.models import UserAlert
from utils.check_status import check_status
from utils.get_live_price import get_live_price_btc

class AlertCreateSerializer(serializers.Serializer):
    ALERT_CHOICES= (
        ("G", "GREATER THAN"),
        ("GE", "GREATER THAN OR EQUAL"),
        ("E", "EQUAL"),
        ("L", "LESS THAN"),
        ("LE", "LESS THAN OR EQUAL"),
    )

    limit = serializers.FloatField()
    alert_on = serializers.ChoiceField(choices = ALERT_CHOICES)

    def validate(self, attrs):
        price = get_live_price_btc()
        if not price:
            raise serializers.ValidationError("Could not find price") 
        if not check_status(attrs['limit'], attrs['alert_on'], price):
            raise serializers.ValidationError("Condition already met")

class AlertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlert
        exclude = ('created_at','updated_at', 'user')

class FilterStatusSerializer(serializers.Serializer):
    status = serializers.CharField()

    def validate(self, attrs):
        if attrs['status'] not in ["A","D","T"]:
            raise serializers.ValidationError("The status is not valid")
        return super().validate(attrs)