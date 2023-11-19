from django.http import JsonResponse

class ResponseHandler:
    @staticmethod
    def success(message, status_code=200):
        return JsonResponse({'status': 'success', 'message': message})

    @staticmethod
    def error(message, status_code=400):
        return JsonResponse({'status': 'error', 'message': message})
