MONGODB_COURSE_DB_NAME="PLMP"
MONGODB_HOST_1="mongodb://localhost:27017"  
front_end_ip = "http://192.168.1.18:3000"
from datetime import timedelta
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=500),
  'ALGORITHM': 'HS256',
  'SIGNING_KEY': 'u22h&79gj6o_q^sd*t(h6lbqc8w!zk!1vbk3b_st$s^97tsn3i',
  'SESSION_COOKIE_DOMAIN' : '172.16.0.208',
  'SESSION_COOKIE_MAX_AGE' : 120000000000,
  'AUTH_COOKIE': 'access_token', 
  'AUTH_COOKIE_SECURE': False,    
  'AUTH_COOKIE_SAMESITE': 'None', 
}