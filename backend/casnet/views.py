from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
import subprocess
import os, sys
import shutil
import base64
from .models import Image, Video
from .serializers import ImageSerializer, VideoSerializer


@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        user_id = request.POST.get('user', '')
        image = request.FILES['image']
        option = request.POST.get('option', '')

        # Save the uploaded image to a temporary location
        image_path = "C:/Pedro/ISEP/PESTI/backend/casnet/00000.jpg"
        with default_storage.open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Define the path to the Python script based on the selected option
        if option == 'casnet1':
            script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/casnet1code.py'
        elif option == 'casnet2':
            script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/casnet2code.py'
        else:
            return JsonResponse({'error': 'Invalid option'}, status=400)
        
        # Verify the paths
        if not os.path.exists(image_path):
            return JsonResponse({'error': f'Image path does not exist: {image_path}'}, status=500)
        if not os.path.exists(script_path):
            return JsonResponse({'error': f'Script path does not exist: {script_path}'}, status=500)

        # Execute the Python script
        try:
            User = get_user_model()
            author = User.objects.get(pk=user_id)
            
            result = subprocess.run(
                ['python', script_path, image_path],
                check=True,
                capture_output=True,
                text=True  # Capture stdout and stderr as strings
            )

            # copy output image to final folder
            output_image = 'C:/Pedro/ISEP/PESTI/backend/casnet/temp.jpg'
            output_path = 'C:/Pedro/ISEP/PESTI/frontend/src/images/created_image.jpg'
            output_path2 = 'C:/Pedro/ISEP/PESTI/frontend/src/assets/created_image.jpg'
            shutil.copy(output_image, output_path)
            shutil.copy(output_image, output_path2)

            
            #save to database
            if os.path.exists(output_image):
                with open(output_image, 'rb') as f:
                    binary_image_data = f.read()
                    processed_image_instance = Image(
                        name=image.name,
                        author=author,
                        image=binary_image_data
                    )
                    processed_image_instance.save()
            
            # Encode the binary image data to base64
            base64_image = base64.b64encode(binary_image_data).decode('utf-8')
            
            # Delete the temporary files
            os.remove(image_path)
            os.remove(output_image)
            
            serializer = ImageSerializer(processed_image_instance)
            return JsonResponse({'image': base64_image, **serializer.data})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt
def process_video(request):
    if request.method == 'POST':
        user_id = request.POST.get('user', '')
        video = request.FILES['video']
        option = request.POST.get('option', '')

        # Save the uploaded video to a temporary location
        video_path = "C:/Pedro/ISEP/PESTI/backend/casnet/temp_video.mp4"
        frames_dir = "C:/Pedro/ISEP/PESTI/backend/casnet/frames"
        processed_frames_dir = "C:/Pedro/ISEP/PESTI/backend/casnet/processed_frames"

        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        if not os.path.exists(processed_frames_dir):
            os.makedirs(processed_frames_dir)

        with default_storage.open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        # Define the paths to the Python scripts
        split_script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/split.py'     
        create_video_script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/create_video.py'
        
        # Define the path to the Python script based on the selected option
        if option == 'casnet1':
            process_script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/casnet1code.py'
        elif option == 'casnet2':
            process_script_path = 'C:/Pedro/ISEP/PESTI/backend/casnet/casnet2code.py'
        else:
            return JsonResponse({'error': 'Invalid option'}, status=400)
        
        # Verify the paths
        if not os.path.exists(video_path):
            return JsonResponse({'error': f'Video path does not exist: {video_path}'}, status=500)
        if not os.path.exists(split_script_path):
            return JsonResponse({'error': f'Split script path does not exist: {split_script_path}'}, status=500)
        if not os.path.exists(process_script_path):
            return JsonResponse({'error': f'Process script path does not exist: {process_script_path}'}, status=500)

        # Execute the split script
        try:
            subprocess.run(
                ['python', split_script_path, video_path, frames_dir],
                check=True,
                capture_output=True,
                text=True 
            )
            
            # start incremental number for output images
            number =1
            
             # Process each frame image
            for frame_file in os.listdir(frames_dir):
                frame_path = os.path.join(frames_dir, frame_file)
                
                process_process = subprocess.run(
                    ['python', process_script_path, frame_path],
                    check=True,
                    capture_output=True,
                    text=True 
                )
                            
                # copy output image to final folder
                output_image = 'C:/Pedro/ISEP/PESTI/backend/casnet/temp.jpg'
                output_path = f'C:/Pedro/ISEP/PESTI/backend/casnet/processed_frames/{str(number).zfill(2)}.jpg'
                shutil.copy(output_image, output_path)
                number+=1;
                
            # Clean up temporary files
            os.remove(video_path)
            
            #create video from output images
            subprocess.run(
                ['python', create_video_script_path, processed_frames_dir],
                check=True,
                capture_output=True,
                text=True 
            )
                      
            # Copy video to final destination
            shutil.copy('created_video.mp4', 'C:/Pedro/ISEP/PESTI/frontend/src/images/created_video.mp4')
            shutil.copy('created_video.mp4', 'C:/Pedro/ISEP/PESTI/frontend/src/assets/created_video.mp4')
            
            # Save the video
            User = get_user_model()
            author = User.objects.get(pk=user_id)
            video_instance = Video(
                    name=video,
                    author=author,
                    video='C:/Pedro/ISEP/PESTI/frontend/src/assets/created_video.mp4'
            )
            video_instance.save()
            
            return JsonResponse({'success': True})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
