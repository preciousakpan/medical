from django.http import JsonResponse

class ResponseHandler:
    @staticmethod
    def success(message):
        return {'status': 'success', 'message': message}

    @staticmethod
    def error(message):
        return {'status': 'error', 'message': message}