
import time
try:
    import jwt
except ModuleNotFoundError as e:
    import os
    os.system("pip install pyjwt")
    import jwt


class JWTToken(object):
    _algorithm = 'HS256'
    _type = 'JWT'
    _issuer = 'AutoRunX'

    def __init__(self, secret_key, expiration_seconds, algorithm=_algorithm) -> None:
        self._secret_key = secret_key
        self._expiration_seconds = expiration_seconds
        self._algorithm = algorithm

    def _header(self):
        return {'alg': self._algorithm, 'typ': self._type}

    def _payload(self, username):
        return {'exp': time.time() + self._expiration_seconds,  # Expiration Time
                'iat': time.time(),  # Issued At
                'iss': self._issuer,  # Issuer
                'data': {'username': username, }
                }

    def generate_token(self, username) -> str:
        return jwt.encode(payload=self._payload(username), key=self._secret_key,
                          algorithm=self._algorithm, headers=self._header())

    def verify_token(self, token) -> tuple[bool,str]:
        try:
            payload = jwt.decode(jwt=token, key=self._secret_key,
                                 algorithms=self._algorithm, issuer=self._issuer)
            return True, payload['data']['username']
        except Exception as e:
            return False, str(e)


