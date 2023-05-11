from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginCredentials(_message.Message):
    __slots__ = ["password", "username"]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    password: str
    username: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ["message", "token"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    message: str
    token: str
    def __init__(self, message: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class SignUpCredentials(_message.Message):
    __slots__ = ["name", "password", "surname", "username"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    password: str
    surname: str
    username: str
    def __init__(self, name: _Optional[str] = ..., surname: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...
