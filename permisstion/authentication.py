from traceback import print_tb
from .token import Token
from rest_framework.permissions import BasePermission
class Authentication(BasePermission):
  def has_permission(self, request, view):
    # print(request.META)
    # print(request.META.get('HTTP_AUTHORIZATION'))
    bear_token = request.META.get('HTTP_AUTHORIZATION')
    if  not bear_token:
      return False
    token = Token.get_token(bear_token)
    if not token:
      return False
    user = Token.validate_token(token)
    if user:
      request.user = user
      return True
    return False