from enum import Enum


class GamAttributeEnum(str, Enum):
    # Generic/common keys
    NAME = "name"
    EMAIL = "email"
    VALUE = "value"
    OWNER = "owner"
    MEMBER = "member"

    # User JSON fields
    PRIMARY_EMAIL = "primaryEmail"
    USERNAME = "user"
    GIVEN_NAME = "givenName"
    FAMILY_NAME = "familyName"
    FULL_NAME = "fullName"
    LANGUAGES = "languages"

    IS_ADMIN = "isAdmin"
    IS_DELEGATED_ADMIN = "isDelegatedAdmin"
    IS_ENROLLED_IN_2SV = "isEnrolledIn2Sv"
    IS_ENFORCED_IN_2SV = "isEnforcedIn2Sv"
    AGREED_TO_TERMS = "agreedToTerms"
    IP_WHITELISTED = "ipWhiteListed"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"
    CHANGE_PASSWORD_AT_NEXT_LOGIN = "changePasswordAtNextLogin"

    ID = "id"
    CUSTOMER_ID = "customerId"
    IS_MAILBOX_SETUP = "isMailboxSetup"
    INCLUDE_IN_GLOBAL_ADDRESS_LIST = "includeInGlobalAddressList"
    CREATION_TIME = "creationTime"
    LAST_LOGIN_TIME = "lastLoginTime"
    ORG_UNIT_PATH = "orgUnitPath"
    RECOVERY_EMAIL = "recoveryEmail"
    THUMBNAIL_PHOTO_URL = "thumbnailPhotoUrl"

    # Collection and nested fields
    GROUPS = "groups"
    GROUP_EMAIL = "groupEmail"

    LICENSES = "licenses"
    LICENSED = "licensed"
    SKU_ID_CAMEL = "skuId"
    SKU_ID = "sku_id"
    SKU = "sku"
    SKU_NAME_CAMEL = "skuName"
    SKU_NAME = "sku_name"
    PRODUCT_NAME = "productName"

    # Patch operations
    REPLACE = "replace"
    ADD = "add"
    REMOVE = "remove"

    # Group creation/update options and values
    ALLOW_EXTERNAL_MEMBERS = "allowExternalMembers"
    WHO_CAN_JOIN = "whoCanJoin"
    WHO_CAN_VIEW_GROUP = "whoCanViewGroup"
    WHO_CAN_POST_MESSAGE = "whoCanPostMessage"

    FALSE = "false"
    CAN_REQUEST_TO_JOIN = "CAN_REQUEST_TO_JOIN"
    ALL_MANAGERS_CAN_VIEW = "ALL_MANAGERS_CAN_VIEW"
    ALL_MANAGERS_CAN_POST = "ALL_MANAGERS_CAN_POST"
