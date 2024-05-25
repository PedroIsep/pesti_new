from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess
import os

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        option = request.POST.get('option', '')

        # Save the uploaded image to a temporary location
        image_path = "C:/Pedro/ISEP/PESTI/backend/casnet/00000.jpg"
        with default_storage.open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Define the path to the Python script
        script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/casnet2code.py'

        # Verify the paths
        if not os.path.exists(image_path):
            return JsonResponse({'error': f'Image path does not exist: {image_path}'}, status=500)
        if not os.path.exists(script_path):
            return JsonResponse({'error': f'Script path does not exist: {script_path}'}, status=500)

        # Execute the Python script
        try:
            result = subprocess.run(
                ['python', script_path, image_path],
                check=True,
                capture_output=True,
                text=True  # Capture stdout and stderr as strings
            )

            # Delete the temporary files
            os.remove(image_path)

            return JsonResponse({'success': True})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
