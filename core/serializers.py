from rest_framework import serializers 
  
class StopSerializer(serializers.Serializer):  
    country = serializers.CharField(max_length=50, required=True)  
    city = serializers.CharField(max_length=50, required=True)  
    activity = serializers.CharField(max_length=500, required=True)  