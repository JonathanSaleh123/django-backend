# auth0authorization/utils.py

import json
import requests
import jwt
from jwt.algorithms import RSAAlgorithm  # ✅ required for from_jwk()

AUTH0_DOMAIN = 'dev-hmrsiaqni4mw8mx7.us.auth0.com'
API_IDENTIFIER = 'https://your-api/'  # 👈 must match Auth0 API identifier
ISSUER = f'https://{AUTH0_DOMAIN}/'

def jwt_decode_token(token):
    # print("🔍 Decoding JWT token...")

    try:
        header = jwt.get_unverified_header(token)
        # print("📦 JWT Header:", header)
    except Exception as e:
        raise Exception(f"Invalid JWT header: {e}")

    try:
        jwks = requests.get(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').json()
        # print("📥 JWKS keys received")
    except Exception as e:
        raise Exception(f"Failed to fetch JWKS: {e}")

    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header.get('kid'):
            # print(f"🔑 Found matching key for kid: {jwk['kid']}")
            public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found in JWKS for kid')

    try:
        decoded = jwt.decode(
            token,
            public_key,
            audience=API_IDENTIFIER,
            issuer=ISSUER,
            algorithms=['RS256']
        )
        # print("✅ Token successfully decoded")
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidAudienceError:
        raise Exception('Invalid audience')
    except jwt.InvalidIssuerError:
        raise Exception('Invalid issuer')
    except jwt.PyJWTError as e:
        raise Exception(f'JWT decode error: {str(e)}')
