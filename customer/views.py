from tkinter.messagebox import NO
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from permisstion.token import Token
from rest_framework.decorators import action
from .serializer import UserSerializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from permisstion.authentication import Authentication
from rest_framework.pagination import PageNumberPagination


class UserViewSet(viewsets.ViewSet, PageNumberPagination):
  queryset = User.objects.all()
  serializer_class = UserSerializers

  @action(methods = ["get"], detail=False, url_path="list", permission_classes=[Authentication])
  def list_user(self, request):
    is_admin = request.user.get("admin", False)
    if not is_admin:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    user = User.objects.all().order_by('-id')
    page = self.paginate_queryset(user, request)
    serializer = UserSerializers(page, many=True)
    return self.get_paginated_response(serializer.data)
  
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

  
  @action(methods = ["POST"], detail=False, url_path="update_password", permission_classes=[Authentication]) 
  def update_password(self, request):
    data = request.data 
    old_password = data.get("old_password", "")
    new_password = data.get("new_password", "")
    username = data.get("username", "")
    avatar = data.get("avatar", "")
    re_check_new_password = data.get("re_check_new_password", "")
    user = get_object_or_404(User, pk=request.user.get('id'))
    if new_password and old_password and re_check_new_password:
      if re_check_new_password != new_password: 
        return Response({"message": "Mật khẩu không trùng khớp"}, status=status.HTTP_400_BAD_REQUEST)          
      if user.username == username and user.check_password(old_password):
        user.password = make_password(new_password)       
      else:
        return Response({"message": "Mật khẩu củ không đúng"}, status=status.HTTP_400_BAD_REQUEST)     
                
    if avatar:
      user.avatar = avatar
      user.save()
      serializer = UserSerializers(user)
      return Response({"message": "Cập nhập thành công", "user": serializer.data}, status=status.HTTP_200_OK)
