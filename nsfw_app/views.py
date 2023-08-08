from django.shortcuts import render

# Create your views here.
import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from nsfw_project import settings
from .nsfw.nsfw_detector import predict

model = predict.load_model('nsfw_app/nsfw/model/')


@csrf_exempt
def upload_and_classify_nsfw(request):
    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']
        file_name = default_storage.save(image.name, ContentFile(image.read()))
        image_path = os.path.join(settings.MEDIA_ROOT, file_name)
        result = predict.classify(model, image_path)
        os.remove(image_path)
        result = list(result.values())[0]

        return JsonResponse({"result": result})

    return JsonResponse({"error": "Invalid request method or missing image"}, status=400)
