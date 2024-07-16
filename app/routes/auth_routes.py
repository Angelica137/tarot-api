from flask import Blueprint, jsonify, request, redirect, session, url_for, current_app
from app.services.user_service import UserService
from urllib.parse import quote_plus, urlencode
import os
from app import oauth
import json
import logging

auth_bp = Blueprint('auth', __name__)


logging.basicConfig(level=logging.INFO)

def get_auth0_client():
    return oauth.register(
        'auth0',
        client_id=current_app.config['AUTH0_CLIENT_ID'],
        client_secret=current_app.config['AUTH0_CLIENT_SECRET'],
        api_base_url=f"https://{current_app.config['AUTH0_DOMAIN']}",
        access_token_url=f"https://{current_app.config['AUTH0_DOMAIN']}/oauth/token",
        authorize_url=f"https://{current_app.config['AUTH0_DOMAIN']}/authorize",
        client_kwargs={
            'scope': 'openid profile email',
        },
        server_metadata_url=f'https://{current_app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
    )

@auth_bp.route('/login')
def login():
    auth0 = get_auth0_client()
    return auth0.authorize_redirect(redirect_uri=url_for('auth.callback', _external=True))

@auth_bp.route('/callback')
def callback():
    auth0 = get_auth0_client()
    token = auth0.authorize_access_token()
    
    # Log the entire token object
    logging.info(f"Full Auth0 token object: {json.dumps(token, indent=2)}")
    
    # Log specific parts of the token
    logging.info(f"Access token: {token.get('access_token', 'Not found')}")
    logging.info(f"ID token: {token.get('id_token', 'Not found')}")
    logging.info(f"Refresh token: {token.get('refresh_token', 'Not found')}")
    
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
    }
    session['access_token'] = token['access_token']
    logging.info(f"Auth0 access token stored in session: {session['access_token'][:10]}...")  # Log first 10 characters

    return redirect('/api/')


@auth_bp.route('/logout')
def logout():
    session.clear()

    params = {
        'returnTo': url_for('api.hello_world', _external=True),  # Assuming you have a route named 'hello_world' in your 'api' blueprint
        'client_id': current_app.config['AUTH0_CLIENT_ID']
    }

    return redirect(
        "https://" + current_app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(params, quote_via=quote_plus)
    )
