from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
import requests
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Настройки Keycloak
keycloak_server_url = "http://localhost:8080/"  # Добавлен слэш в конце
realm_name = "myrealm"
client_id = "myrealm"
client_secret = "p0wkUtW2abAXgYN284eR0t53yNKGQ3Xn"

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

origins = [
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Маршрут для перенаправления на страницу аутентификации Keycloak
@app.get("/login")
async def login():
    redirect_uri = "http://localhost:8000/callback"  # Замените на ваш реальный адрес приложения
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid"
    }
    try:
        auth_url = requests.Request('GET', keycloak_auth_url, params=params).prepare().url
        if auth_url:
            return RedirectResponse(url=auth_url)
        else:
            raise HTTPException(status_code=500, detail="Не удалось сформировать URL для аутентификации")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при получении URL аутентификации")

# Маршрут для обработки обратного вызова (callback) от Keycloak
@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="Код авторизации не найден")

    # Обмен кода авторизации на токен доступа
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://localhost:8000/callback",  # Замените на ваш реальный адрес
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(keycloak_token_url, data=token_data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Не удалось получить токен доступа")

    token = response.json()
    access_token = token.get('access_token')
    if not access_token:
        raise HTTPException(status_code=400, detail="Токен доступа не найден в ответе")

    # Сохранение токена в cookie (например)
    response = RedirectResponse(url="/user")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

# Защищенный маршрут для получения информации о пользователе
@app.get("/user")
async def get_user_info(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")

    try:
        # Валидация токена и получение информации о пользователе
        userinfo = keycloak_openid.userinfo(access_token)
        username = userinfo.get('preferred_username', 'User')

        # Получение разрешений пользователя
        # user_permissions  = keycloak_openid.uma_permissions(access_token)
        return userinfo

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Ошибка при запросе к Keycloak")

    except KeyError as e:
        raise HTTPException(status_code=500, detail="Неверный формат ответа от Keycloak")

    except Exception as e:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

# Корневой маршрут для перенаправления на фронтэнд Quasar
@app.get("/")
async def root():
    return RedirectResponse(url="http://localhost:9000/#/")  # Замените на URL вашего фронтенда Quasar

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

    # Выводим информацию о порте
    print(f"FastAPI запущен на порту 8000")
