from tkinter.messagebox import NO
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from permisstion.token import Token
from rest_framework.decorators import action
from .serializer import UserSerializers
# Create your views here.
class UserViewSet(viewsets.ViewSet):

  def list(self, request):
    return Response({"message": "ok"})
  
  def create(self, request):
    data = request.data 
    serializer = UserSerializers(data= data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response({"message": "Create User success"}, status=status.HTTP_200_OK)

  @action(methods = ["POST"], detail=False, url_path="login")
  def login(self, request):
    data = request.data 
    password = data.get('password', None)
    username = data.get('username', None)
    
    if not password or not username:
      return Response({"message": "username and password is not none"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(username = username).first()
    if user:
      if user.check_password(password):
        token = Token.generate_token(user)
        serializer = UserSerializers(user)
        return Response({"message": "Login successs", "token": token, "user": serializer.data}, status=status.HTTP_200_OK)
       
    return Response({"message": "User is not exists"}, status=status.HTTP_400_BAD_REQUEST)
