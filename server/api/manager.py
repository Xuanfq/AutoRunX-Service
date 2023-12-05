
from .lib.jwttoken import JWTToken
from .arxapp import AppManager
import os
from . import settings

TOKEN_CENTER_SECRET_KEY = settings.TOKEN_CENTER['SECRET_KEY']
TOKEN_CENTER_EXPIRE_TIME = settings.TOKEN_CENTER['EXPIRE_TIME']

APP_MANAGER_APP_BASE_PATH = settings.APP_MANAGER['APP_BASE_PATH']
APP_MANAGER_MAX_APP_NUMBER = settings.APP_MANAGER['MAX_APP_NUMBER']
APP_MANAGER_WEBSOCKET_PORT = settings.APP_MANAGER['WEBSOCKET']['port']
APP_MANAGER_WEBSOCKET_OPEN = settings.APP_MANAGER['WEBSOCKET']['open']


# token center
tokencenter = JWTToken(secret_key=TOKEN_CENTER_SECRET_KEY,
                       expiration_seconds=TOKEN_CENTER_EXPIRE_TIME)

# app manager
appmanager = AppManager(app_base_path=APP_MANAGER_APP_BASE_PATH,
                        websocket_support=APP_MANAGER_WEBSOCKET_OPEN,
                        websocket_port=APP_MANAGER_WEBSOCKET_PORT,
                        max_app_num=APP_MANAGER_MAX_APP_NUMBER,
                        token_auth_funcion=tokencenter.verify_token)
