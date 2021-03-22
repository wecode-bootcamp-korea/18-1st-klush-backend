import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self,request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            name         = data['name']
            phone_number = data['phone_number']
            nickname     = data.get('nickname', None)

            if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone_number=phone_number)).exists():
                return JsonResponse({'message':'DUPLICATED_INFORMATION'}, status=400)

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{10,25}'
            regex_name     = '^[ㄱ-ㅎ|가-힣|a-z|A-Z]{2,20}$'
            regex_phone    = '^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$'

            if not re.match(regex_email,email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if not re.match(regex_password,password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            if not re.match(regex_name,name):
                return JsonResponse({'message':'INVALID_NAME'}, status=400)

            if not re.match(regex_phone,phone_number):
                return JsonResponse({'message':'INVALID_PHONENUMBER'}, status=400)

            bycrpted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password  = bycrpted_password.decode('utf-8')
            
            User.objects.create(
                email        = email,
                password     = decoded_password,
                name         = name,
                phone_number = phone_number,
                nickname     = nickname
                )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)