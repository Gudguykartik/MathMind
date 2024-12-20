from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import base64
from io import BytesIO
from PIL import Image
from .utils import analyze_image
import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')

def results(request):
    # Get results from session
    results_data = request.session.get('math_results', {})
    # Clear the session data after retrieving it
    if 'math_results' in request.session:
        del request.session['math_results']
    return render(request, 'results.html', {'results': results_data})

@csrf_exempt
@require_http_methods(["POST"])
def process_image(request):
    try:
        # Log request content type and body
        logger.info(f"Content-Type: {request.content_type}")
        logger.info(f"Request body: {request.body[:100]}...")

        # Get JSON data from request body
        try:
            data = json.loads(request.body)
            logger.info("Parsed data successfully")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({
                "message": f"Invalid JSON data: {str(e)}",
                "status": "error"
            }, status=400)

        # Check if image data exists
        if 'image' not in data:
            logger.error("No image data in request")
            return JsonResponse({
                "message": "No image data provided",
                "status": "error"
            }, status=400)

        # Extract base64 image data
        try:
            image_data = data['image']
            logger.info(f"Image data prefix: {image_data[:30]}...")
            
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = BytesIO(base64.b64decode(image_data))
            image = Image.open(image_bytes)
            logger.info(f"Image opened successfully: {image.size}")
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return JsonResponse({
                "message": f"Error processing image: {str(e)}",
                "status": "error"
            }, status=400)

        dict_of_vars = data.get('dict_of_vars', {})
        logger.info(f"Variables dictionary: {dict_of_vars}")
        
        try:
            responses = analyze_image(image, dict_of_vars=dict_of_vars)
            logger.info(f"Analysis responses: {responses}")
            
            # Store results in session
            request.session['math_results'] = {
                "message": "Image processed successfully",
                "data": responses,
                "status": "success"
            }
            
            return JsonResponse({
                "message": "Image processed successfully",
                "redirect": "/results/",
                "status": "success"
            })
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return JsonResponse({
                "message": f"Error analyzing image: {str(e)}",
                "status": "error"
            }, status=500)

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return JsonResponse({
            "message": f"Server error: {str(e)}",
            "status": "error"
        }, status=500)