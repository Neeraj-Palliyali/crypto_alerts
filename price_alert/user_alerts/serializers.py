from rest_framework import serializers
import requests
import json

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
        url  = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        response = requests.get(url=url)
        data = json.loads(response.text)
        for i in data:
            if i.get('id') == 'bitcoin':
                price = i.get('current_price')
                if check_status(attrs['limit'], attrs['alert_on'], price):
                    return super().validate(attrs)
                else:
                    raise serializers.ValidationError("Condition already met")
        raise serializers.ValidationError("Error in finding bitcoin price")

def check_status(limit, alert_on, current_val):
    if alert_on == "G":
        val = False if current_val > limit else  True 

    elif  alert_on == "GE":        
        val = False if current_val >= limit else  True 

    elif  alert_on == "E":        
        val = False if current_val == limit else  True 
    
    elif  alert_on == "LE":        
        val = False if current_val <= limit else  True 
    
    elif  alert_on == "L":        
        val = False if current_val < limit else  True 

    return val