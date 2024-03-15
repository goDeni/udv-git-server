from base64 import decodebytes
from enum import Enum
from http import HTTPStatus
from typing import Annotated, Optional
from urllib.parse import parse_qsl, urlparse

from fastapi import FastAPI, Header, Response
from uvicorn import Config, Server

app = FastAPI()

_USERS = {
    'user': '123',
    '1': '1',
}

_AuthorizationHeader = Header(examples=['Basic MjEzOjEyMw=='])
_OriginUrlHeader = Header(
    alias='x-original-uri',
    examples=[
        '/first.git/info/refs?service=git-upload-pack',
    ],
)


@app.get('/auth')
def _handle_auth(
    original_uri: Annotated[str, _OriginUrlHeader],
    authorization: Annotated[Optional[str], _AuthorizationHeader] = None,
) -> Response:
    print('authorization', authorization)  # noqa: T201
    if authorization is not None and authorization.lower().startswith('basic'):
        token = authorization.rsplit(maxsplit=1)[-1]

        auth_data = decodebytes(token.encode('utf-8')).decode('utf-8')
        print('Auth data', auth_data)  # noqa: T201
        login, unused_sep, password = auth_data.partition(':')
        if login and password and _USERS.get(login) == password:
            print('User ok')  # noqa: T201
            _assert_permissions(login, original_uri)
            return Response(status_code=HTTPStatus.NO_CONTENT)

    return Response(status_code=HTTPStatus.UNAUTHORIZED, headers={'WWW-Authenticate': 'Basic realm="Git login"'})


class _GitService(str, Enum):
    # git pull/clone/fetch
    GIT_UPLOAD_PACK = 'git-upload-pack'
    # git push
    GIT_RECEIVE_PACK = 'git-receive-pack'


def _read_service(uri: str) -> _GitService:
    result = urlparse(uri)
    query_params = dict(parse_qsl(result.query))
    if service := query_params.get('service'):
        return _GitService(service)

    service = uri.rsplit('/', maxsplit=1)[-1]
    return _GitService(service)


def _assert_permissions(login: str, uri: str):
    print('Check', uri)  # noqa: T201
    service = _read_service(uri)
    print(f'User "{login}" use service', service)  # noqa: T201


def main():
    Server(
        Config(
            app=app,
            port=8090,
        ),
    ).run()


if __name__ == '__main__':
    main()
