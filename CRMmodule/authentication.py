from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        print(f"Заголовок Authorization: {request.headers.get('Authorization')}")
        return super().authenticate(request)