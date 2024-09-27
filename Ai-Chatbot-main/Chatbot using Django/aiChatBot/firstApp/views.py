import json
import os
import csv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "index.html")

def csv_to_json(csv_file_path):
    data = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return data

def load_responses():
    responses = {}
    responses_path = os.path.join(os.path.dirname(__file__), 'responses.json')
    try:
        with open(responses_path, 'r') as file:
            responses = json.load(file)
    except Exception as e:
        print(f"Error loading responses: {e}")
    return responses

def load_universities():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'hte.csv')
    universities = csv_to_json(csv_file_path)
    print(f"Loaded universities: {universities}")  # Debugging line
    return universities

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            print(f"User message: {user_message}")  # Debugging line

            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Load university data and responses
            universities = load_universities()
            responses = load_responses()

            # Get the bot reply using the custom logic
            bot_reply = generate_bot_reply(user_message, universities, responses)
            print(f"Bot reply: {bot_reply}")  # Debugging line

            return JsonResponse({'reply': bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
def generate_bot_reply(message, universities, responses):
    message = message.lower()

    # Check for greetings
    greetings_keywords = ["hi", "hello", "hey", "greetings"]
    if any(greet in message for greet in greetings_keywords):
        return responses.get("greetings", "Hello! How can I assist you today?")

    # Check for university inquiries
    for university in universities:
        university_name = university['University Name'].lower()
        # Check if any part of the university name is in the user message
        if university_name in message:
            contact = university['Contact No.']
            website = university['Website Links']
            # Ensure the website link starts with http:// or https://
            if not website.startswith("http"):
                website = "http://" + website
            # Format the response with a hyperlink
            return (
                f"{university['University Name']} - Contact: {contact}, "
                f"Website: <a href='{website}' target='_blank' style='color: white; text-decoration: underline;'>{website}</a>"
            )

    # Check for other responses
    for key in responses.keys():
        if key.lower() in message:
            return responses[key]

    return responses.get("other_key", "I'm sorry, I didn't understand that.")
