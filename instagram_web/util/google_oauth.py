from app import app
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

oauth.register('google',
    client_id=app.config.get("G_CLIENT_ID"),
    client_secret=app.config.get("G_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)