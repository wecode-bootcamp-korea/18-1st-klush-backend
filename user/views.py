import json, re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data.get('email')
            password = data['password']
            

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{10,25}'

            if not re.match(regex_email,email):
                return JsonResponse({'message':'잘못된 형식입니다. 이메일을 다시 한번 확인해 주세요'}, status=400)

            if not re.match(regex_password,password):
                return JsonResponse({'message':'비밀번호는 10자리 이상, 영문과 숫자, 특수문자를 모두 입력해주세요.'})

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'유효하지 않은 비밀번호 입니다.'}, status=401)

            access_token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'token': access_token, 'name': user.name, 'message':'로그인 되었습니다.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSONDECODE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except User.MultipleObjectsReturned:
            return JsonResponse({'message':'INVALID_USER, get() returned more than one -- it returned 2!'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
