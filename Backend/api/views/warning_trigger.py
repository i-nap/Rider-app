from ..utils.kafka_producer import send_warning_event
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def warning_trigger(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        send_warning_event(payload)
        return JsonResponse({'message': 'Warning event sent to Kafka'})
