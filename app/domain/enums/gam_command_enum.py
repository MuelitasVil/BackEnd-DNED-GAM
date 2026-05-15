from enum import Enum


class GamCommandEnum(str, Enum):
    GAM = "gam"
    VERSION = "version"

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    INFO = "info"

    USER = "user"
    GROUP = "group"
    LICENSE = "license"

    ADD = "add"
    REMOVE = "remove"

    JSON = "json"
    FILE = "file"
    FORMAT_JSON = "formatjson"
    PREVIEW = "preview"

    OU = "ou"
    GROUPS = "groups"

    SUSPEND = "suspend"
    UNSUSPEND = "unsuspend"
