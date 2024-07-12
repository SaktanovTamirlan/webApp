from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
import requests
import uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Настройки Keycloak
keycloak_server_url = "http://localhost:8080/"
realm_name = "myrealm"
client_id = "myrealm"
client_secret = "KjZHbVbjBHo4UZ5ocU2SjnJs1kOguF8o"

# Инициализация Keycloak клиента
keycloak_openid = KeycloakOpenID(server_url=keycloak_server_url,
                                realm_name=realm_name,
                                client_id=client_id,
                                client_secret_key=client_secret)

# URL для аутентификации через Keycloak
keycloak_auth_url = f"{keycloak_server_url}realms/{realm_name}/protocol/openid-connect/auth"
keycloak_token_url = f"{keycloak_server_url}realms/{realm_name}/protocol/openid-connect/token"

# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/login")
async def login():
    redirect_uri = "http://localhost:8000/callback"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid"
    }
    try:
        auth_url = requests.Request('GET', keycloak_auth_url, params=params).prepare().url
        if auth_url:
            logging.debug(f"Auth URL: {auth_url}")
            return RedirectResponse(url=auth_url)
        else:
            raise HTTPException(status_code=500, detail="Не удалось сформировать URL для аутентификации")
    except Exception as e:
        logging.error(f"Ошибка при получении URL аутентификации: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении URL аутентификации")

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Код авторизации не найден")

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://localhost:8000/callback",
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(keycloak_token_url, data=token_data)
    if response.status_code != 200:
        logging.error(f"Не удалось получить токен доступа, статус: {response.status_code}, ответ: {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Не удалось получить токен доступа")

    token = response.json()
    access_token = token.get('access_token')
    if not access_token:
        logging.error("Токен доступа не найден в ответе")
        raise HTTPException(status_code=400, detail="Токен доступа не найден в ответе")

    response = RedirectResponse(url="/user")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/user")
async def get_user_info(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")

    try:
        userinfo = keycloak_openid.userinfo(access_token)
        username = userinfo.get('preferred_username', 'User')
        return RedirectResponse(url="http://localhost:9000/#/")
    except Exception as e:
        logging.error(f"Неверные учетные данные: {e}")
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

@app.get("/")
async def root():
    return RedirectResponse(url="http://localhost:9000/#/")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
