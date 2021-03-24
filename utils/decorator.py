import json
import bcrypt
import jwt

from user.models import User

from my_settings import SECRET_KEY, ALGORITHM

def authorization (func):
    def wrapper (self, request, *args, **kwargs):
        try:
            token         = request.headers['Authorization']
            decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)

            if not User.objects.filter(id=decoded_token["user_id"]).exists():
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

            request.user  = User.objects.get(id=decoded_token["user_id"])
            return func(self, request, *args, **kwargs)
            
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
    return wrapper