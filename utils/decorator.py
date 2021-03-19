import json
import bcrypt
import jwt

from user.models import User

from my_settings import SECRET_KEY, ALGORITHM

def authorization (func):
    def wrapper (self, request, *args, **kwrgs):
        try:
            token = request.headers['Authorization']
            decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
            request.user = User.objects.get(id=decoded_token["user_id"])
            return func(self, request, *args, **kwargs)
            
        except ValueError:
            return JsonResponse({'message':'It returned None instead.'}, status=400)

        except jwt.DecodeError:
            return JsonResponse({'message': 'Not exact token'}, status=400)
    return wrapper