from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .serializers import StopSerializer

from cohere import Client
import json

from dotenv import load_dotenv
import os
 
load_dotenv()
  
# Endpoint from frontend to send user's data
# It is possible for activity AND/OR country/city to be empty
class StopView(APIView):  
    def post(self, request):

        serializer = StopSerializer(data=request.data, many=True)  
        if serializer.is_valid():
            plan = prompt_for_plan(request.data)
            return Response({"status": "success", "data": plan}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class Stop:
    def __init__(self, country, city, activity):
        self.country = country
        self.city = city
        self.activity = activity

    def __str__(self):
        return f'Country: {self.country}   City: {self.city}   Activity: {self.activity}'

def prompt_for_plan(stops):
    client = Client(client_name="Deltahacks", api_key=os.getenv('COHERE_API_KEY'), )        

    prompt="Fill in the missing fields in the following trip plan to create a detailed itinerary. For each entry, suggest a city or activity if they are empty, if the activity is generic and not a specific activity suggest a specific activity and location.\n\n"

    for stop in stops:
        prompt+= f"Country: {stop['country']}, City: {stop['city']}, Activities: {stop['activity']}\n"

    prompt += "\nGenerate a complete trip plan with countries, cities, and activities."

    prompt += '''
    Format the response as a nested dictionary where:
    1. The first level is the country.
    2. The second level is the city in that country.
    3. The third level is the activity in that city.
    
    Here is the list of locations:
    {', '.join(location_names)}

    Example output format:
    {{
      "USA": {{
        "New York": {{
          "Visit Statue of Liberty": {{}},
          "Walk through Central Park": {{}}
        }},
        "Los Angeles": {{
          "Visit Hollywood Walk of Fame": {{}},
          "See the Griffith Observatory": {{}}
        }}
      }},
      "Japan": {{
        "Tokyo": {{
          "Explore Shibuya Crossing": {{}},
          "Visit the Tokyo Skytree": {{}}
        }}
      }}
    }}
    '''

    response = client.chat(
	message=prompt,
	model="command-r-08-2024",
	preamble="You are an AI-assistant chatbot. You are trained to assist users by providing thorough and helpful responses to their queries. Do not suggest more activities if the the activity value is not empty."
    )

    return response