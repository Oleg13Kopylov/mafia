from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class check_if_game_is_finished_reply(_message.Message):
    __slots__ = ["ans_bool", "ans_str"]
    ANS_BOOL_FIELD_NUMBER: _ClassVar[int]
    ANS_STR_FIELD_NUMBER: _ClassVar[int]
    ans_bool: bool
    ans_str: str
    def __init__(self, ans_bool: bool = ..., ans_str: _Optional[str] = ...) -> None: ...

class check_if_game_is_finished_request(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    def __init__(self, room_id: _Optional[int] = ...) -> None: ...

class empty_reply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class empty_request(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class has_game_started(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    def __init__(self, room_id: _Optional[int] = ...) -> None: ...

class reply_all(_message.Message):
    __slots__ = ["str"]
    STR_FIELD_NUMBER: _ClassVar[int]
    str: str
    def __init__(self, str: _Optional[str] = ...) -> None: ...

class reply_bool(_message.Message):
    __slots__ = ["ans_bool"]
    ANS_BOOL_FIELD_NUMBER: _ClassVar[int]
    ans_bool: bool
    def __init__(self, ans_bool: bool = ...) -> None: ...

class reply_check(_message.Message):
    __slots__ = ["ans", "validity"]
    ANS_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    ans: bool
    validity: bool
    def __init__(self, validity: bool = ..., ans: bool = ...) -> None: ...

class reply_event(_message.Message):
    __slots__ = ["event_type", "message"]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    event_type: int
    message: str
    def __init__(self, event_type: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class reply_int(_message.Message):
    __slots__ = ["int"]
    INT_FIELD_NUMBER: _ClassVar[int]
    int: int
    def __init__(self, int: _Optional[int] = ...) -> None: ...

class reply_room_id(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    def __init__(self, room_id: _Optional[int] = ...) -> None: ...

class reply_str(_message.Message):
    __slots__ = ["str"]
    STR_FIELD_NUMBER: _ClassVar[int]
    str: str
    def __init__(self, str: _Optional[str] = ...) -> None: ...

class request_room_id(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class request_to_check(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_end_day(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_end_night(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_execute(_message.Message):
    __slots__ = ["is_ghost", "name", "room_id"]
    IS_GHOST_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    is_ghost: bool
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ..., is_ghost: bool = ...) -> None: ...

class request_to_get_alive_users(_message.Message):
    __slots__ = ["room_id"]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: int
    def __init__(self, room_id: _Optional[int] = ...) -> None: ...

class request_to_get_role(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_join(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_kill(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_leave(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_publish(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_start_day(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_to_start_night(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class request_updates(_message.Message):
    __slots__ = ["name", "room_id"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    room_id: int
    def __init__(self, name: _Optional[str] = ..., room_id: _Optional[int] = ...) -> None: ...

class response_to_execute(_message.Message):
    __slots__ = ["name_of_executed", "validity"]
    NAME_OF_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    VALIDITY_FIELD_NUMBER: _ClassVar[int]
    name_of_executed: str
    validity: bool
    def __init__(self, validity: bool = ..., name_of_executed: _Optional[str] = ...) -> None: ...
