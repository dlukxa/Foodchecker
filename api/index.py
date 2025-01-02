from flask import Flask, request, jsonify
import google.generativeai as genai
from google.generativeai.types import ContentType
from PIL import Image
import requests
from io import BytesIO
import json
from flask_cors import CORS, cross_origin  # Import CORS

app = Flask(__name__)
CORS(app)  # Initialize CORS with app

# Initialize your Gemini model (replace with your actual model name)
GOOGLE_API_KEY = 'AIzaSyCk0zQRKEIDRTBPSDpeGuwIE2e8TRvBaJw'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Create a file to store image URLs
#image_urls_file = 'image_urls.txt'


@app.route('/')
@app.route('/generate', methods=['GET'])
@cross_origin() # Enable CORS for this route
def generate_text():
    print('start')
    url = request.args.get('img')
    print(url)
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        response = requests.get(url)
        url = "https://api.weektopic.org/?url=https://firebasestorage.googleapis.com/v0/b/calories-estimator.appspot.com/o/One-pot-chicken-and-rice-62e986b.jpg?alt=media&token=04d11b27-1377-4aaa-b3b4-e9b843aaad90"
        img = Image.open(BytesIO(response.content))

        prompt = ["Using an image of a meal, I need to estimate its caloric content. Please identify all visible ingredients, estimate their portion sizes using common object comparisons, and suggest likely cooking methods. Calculate the calorie count for each component using a standard calorie database and provide a total caloric estimate for the meal. Additionally, offer a brief overview of the meal's nutritional content, focusing on macronutrients and significant micronutrients. This comprehensive analysis will help in understanding the meal's nutritional impact and making informed dietary decisions. result give as json format. in resposne do not it have any this word 'json'. No empty in first line", img]

        model_response = model.generate_content(prompt)
        print(model_response.text)
        response = model_response.text

        # Splitting the string into lines, stripping leading spaces, and filtering out empty lines
        cleaned_lines = [line.lstrip() for line in response.splitlines() if line.strip()]

        # Joining the cleaned lines back into a single string
        cleaned_string = '\n'.join(cleaned_lines)


        try:
            json_data = json.loads(cleaned_string)
            return jsonify(json_data)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            print("Raw response:", json_data)  # Log the raw response for debugging
            return jsonify({'error': 'Invalid JSON data received', 'details': str(e)}), 500
        except Exception as e:
            print("Unexpected error:", e)
            return jsonify({'error': str(e)}), 500


    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)