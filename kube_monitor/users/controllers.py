from users.serializers import UserSerializer, UserRegisterSerializer
from users.models import UserRegister
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
import pdb


class UserController:

    def get_user_info_list(self, request):
        if request.user.is_superuser:
            try:
                obj = UserRegister.objects.all()
                serializer_user = UserRegisterSerializer(obj, many=True)
                data = json.dumps(serializer_user.data)
                result = {"status": "200_OK", "data": data}
                return json.dumps(result)
            except Exception as error:
                print(error)
        else:
            data = "You dont have credentials to see all data"
            result = {"status": "403_Forbidden", "data": data}
            return json.dumps(result)

    def get_user_info(self, request, pk):
        if pk == request.user.username:
            try:
                obj = UserRegister.objects.get(user_id=request.user.id)
                serializer_user = UserRegisterSerializer(obj)
                data = json.dumps(serializer_user.data)
                result = {"status": "200_OK", "data": data}
                return json.dumps(result)
            except Exception as error:
                print(error)
        else:
            data = "Please provide your valid username"
            result = {"status": "404_NotFound", "data": data}
            return json.dumps(result)

    def register(self, request):
        data = request.data
        try:
            User.objects.get(username=data.get("username"))
            data = {"status": "User ID already Exist"}
            result = {"status": "409_Conflict", "data": data}
            return json.dumps(result)

        except User.DoesNotExist:
            user = User.objects.create_user(data.get("username"), data.get("email"), data.get("password"))
            register = UserRegister()
            user.first_name = data.get('fname', '')
            user.last_name = data.get('lname', '')
            user.is_staff = True
            user.is_active = True
            register.user = user
            register.mobile_no = data.get("mobile", '')
            register.hometown = data.get("hometown", '')
            register.save()
            user.save()
            data = json.dumps({"status": " Registration success! Please Log In"})
            result = {"status": "201_created", "data": data}
            return json.dumps(result)

        except:
            data = json.dumps({"status": " Registration failed! Please check the entry details"})
            result = {"status": "400_BadRequest", "data": data}
            return json.dumps(result)

    def user_update(self, request, pk):
        data = request.data
        if data.get("username") == request.user.username:
            try:
                user = User.objects.get(username=data.get("username"))
                user.set_password = data.get('password', '')
                user.email = data.get('email', '')
                user.last_name = data.get('lname', '')
                user.first_name = data.get('fname', '')
                user.last_name = data.get('lname', '')
                register = UserRegister.objects.get(user_id=request.user.id)
                register.mobile_no = data.get("mobile", '')
                register.hometown = data.get("hometown", '')
                register.save()
                user.save()
                data = "Update success!"
                result = {"status": "200_OK", "data": data}
                return json.dumps(result)
            except Exception as error:
                print(error)
        else:
            data = "Please provide your valid username.\nNote: Username can't be changed"
            result = {"status": "404_NotFound", "data": data}
            return json.dumps(result)

    def user_delete(self, request, pk):
        if pk == request.user.username:
            try:
                user = User.objects.get(username=request.user.username)
                register = UserRegister.objects.get(user_id=request.user.id)
                register.delete()
                user.delete()
                data = "Deleted Success!"
                result = {"status": "200_OK", "data": data}
                return json.dumps(result)
            except Exception as error:
                print(error)
        else:
            data = "Please provide your valid username"
            result = {"status": "400_BadRequest", "data": data}
            return json.dumps(result)
