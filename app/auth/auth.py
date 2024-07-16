import os
from dotenv import load_dotenv
import json
from flask import request, abort
from functools import wraps
from flask.json import jsonify
from jose import jwt
from urllib.request import urlopen

# Get the path to the .env file
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(os.path.dirname(os.path.dirname(basedir)), '.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
ALGORITHMS = os.environ.get('ALGORITHMS', 'RS256').split(',')
database_path = os.environ.get('DATABASE_URL')


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    """Obtains the Access Token from the Authorisation Header"""
    # Get teh authorisation header fomr the request
    auth = request.headers.get('Authorization', None)
    print(f"Authorisation headder: {auth}")

    # raise an error if no header is present
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print("No permissions in payload")
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        print(
            f"Required permission '{permission}' not in payload permissions: \
            {payload['permissions']}")
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    print(f"Permission '{permission}' found in payload")
    return True


def verify_decode_jwt(token):
    # get the public key from Auth0
    print(f"Verifying token: {token[:10]}...")
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get data in header
    unverified_header = jwt.get_unverified_header(token)
    print(f"Unverified header: {unverified_header}")

    # Choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            print(f"Token successfully decoded. Payload: {payload}")

            print(f"Token successfully decoded. Payload: {payload}")
            return payload

        except jwt.ExpiredSignatureError:
            print("Token expired")
            raise AuthError({
                'code': 'token+expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError as e:
            print(f"JWTClaimsError: {str(e)}")
            print(f"Expected audience: {API_AUDIENCE}")
            print(f"Expected issuer: https://{AUTH0_DOMAIN}/")
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience \
                and issuer'
            }, 401)
        except Exception as e:
            print(f"Exception in token decoding: {str(e)}")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    print("No RSA key found")
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"Checking permission: {permission}")
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                print(f"JWT payload: {payload}")
            except Exception as e:
                print(f"JWT verification failed: {e}")
                abort(401)

            try:
                check_permissions(permission, payload)
                print("Permission check passed")
            except Exception as e:
                print(f"Permission check failed: {e}")
                abort(403)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
