import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data.get('email')
            password = data['password']

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{10,25}'

            if not re.match(regex_email,email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=401)

            if not re.match(regex_password,password):
                return JsonResponse({'message':'INVALID_PASSWORD'},status=401)

            if not User.objects.filter(email=email).exist():
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'token': access_token, 'name': user.name, 'message':'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSONDECODE_ERROR'}, status=400)

        except User.MultipleObjectsReturned:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
