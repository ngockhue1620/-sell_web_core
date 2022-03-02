import jwt
from django.conf import settings
class Token():
  def generate_token(user):    
    private_key = settings.PRIVATE_KEY
    user = {
      "id": user.id,
    }
    token = jwt.encode(user, private_key, algorithm="RS256")
    return token

  def validate_token(token):
    public_key = settings.PUBLIC_KEY
    try:
      is_right_token = jwt.decode(token, public_key, algorithms=["RS256"])
      if is_right_token:
        return is_right_token
      return False
    except Exception as e:
      return False
  
  def get_token(value):
    try:
      token = value.split(' ')[1]
      return token
    except:
      return False
    