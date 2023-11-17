from django.http import JsonResponse

class ResponseHandler:
    @staticmethod
    def success(message):
        return JsonResponse({'status': 'success', 'message': message})

    @staticmethod
    def error(message):
        return JsonResponse({'status': 'error', 'message': message})
