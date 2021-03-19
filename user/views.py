import json, re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

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
                return JsonResponse({'message':' 이미 가입되어 있습니다.'}, status=400)

            regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{10,25}'
            regex_name = '^[ㄱ-ㅎ|가-힣|a-z|A-Z]{2,20}$'
            regex_phone = '^[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}$'

            if not re.match(regex_email,email):
                return JsonResponse({'message':'잘못된 형식입니다. 이메일을 다시 한번 확인해 주세요'}, status=400)

            if not re.match(regex_password,password):
                return JsonResponse({'message':'비밀번호는 10자리 이상, 영문과 숫자만 가능합니다'})

            password         = data['password'].encode('utf-8')
            password_crypt   = bcrypt.hashpw(password, bcrypt.gensalt())
            decoded_password = password_crypt.decode('utf-8')

            if not re.match(regex_name,name):
                return JsonResponse({'message':'이름을 다시 한번 확인해 주세요'}, status=400)

            if not re.match(regex_phone,phone_number):
                return JsonResponse({'message':'핸드폰번호를 다시 한번 확인해주세요'}, status=400)

            User.objects.create(email=email, password=decoded_password, name=name, phone_number=phone_number, nickname=nickname)
            return JsonResponse({'message':'회원가입 되었습니다.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
