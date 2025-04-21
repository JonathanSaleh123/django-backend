# auth0authorization/utils.py

import json

import jwt
import requests

def jwt_decode_token(token):
    print("🔍 Decoding JWT token...")
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-hmrsiaqni4mw8mx7.us.auth0.com')).json()
    public_key = None
    print("🔑 Looking for public key in JWKS...")

    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            print(f"🔑 Found matching key with kid:")
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            print("✅ Public key found!")
            
    if public_key is None:
        print("🔥 Public key not found in JWKS")
        raise Exception('Public key not found.')
    print("🔐 Verifying JWT token...")
    issuer = 'https://{}/'.format('dev-hmrsiaqni4mw8mx7.us.auth0.com')
    return jwt.decode(token, public_key, audience='https://your-api/', issuer=issuer, algorithms=['RS256'])