from traceback import print_tb
from .token import Token
from rest_framework.permissions import BasePermission
class Authentication(BasePermission):
  def has_permission(self, request, view):
    # print(request.META)
    # print(request.META.get('HTTP_AUTHORIZATION'))
    bear_token = request.META.get('HTTP_AUTHORIZATION')
    token = Token.get_token(bear_token)
    is_alow = Token.validate_token(token)
    if is_alow:
      return True
    return False