
import os

TOKEN_CENTER={
    'SECRET_KEY': 'rxGztJqAVAMt1i6hOZ63k8uITHq6f2UgjSUHXcVFt6y5kp7noHVpPVt553CofZ0c',
    'EXPIRE_TIME': 3600*24*7,
}

APP_MANAGER = {
    'APP_BASE_PATH': os.path.join(os.getcwd(), 'media'),
    'MAX_APP_NUMBER': 999999,
    'WEBSOCKET': {
        'open': True,
        'port': 8765
    }
}
