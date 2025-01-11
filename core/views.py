from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .serializers import StopSerializer
  
# Endpoint from frontend to send user's data
# It is possible for activity AND/OR country/city to be empty
class StopView(APIView):  
    def post(self, request):

        serializer = StopSerializer(data=request.data, many=True)  
        if serializer.is_valid():
            build_request(request.data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class Stop:
    def __init__(self, country, city, activity):
        self.country = country
        self.city = city
        self.activity = activity

    def __str__(self):
        return f'Country: {self.country}   City: {self.city}   Activity: {self.activity}'
    
def build_request(stops):
    for s in stops:
        stop = Stop(country=s.get('country'), city=s.get('city'), activity=s.get('activity'))
        print(stop)