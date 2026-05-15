import subprocess
import json
import tempfile
from typing import List, Optional, Dict, Any

from app.domain.dtos.gam import (
    GamUserDto,
    GamUserSettings,
    GamUserGroup,
    GamUserLicense,
    GamUserQuotaDto,
)
from app.domain.enums.gam_command_enum import GamCommandEnum
from app.domain.enums.gam_attribute_enum import GamAttributeEnum


def _run_gam_command(args: List[str]) -> str:
    cmd = [GamCommandEnum.GAM.value] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"GAM command failed: {' '.join(cmd)} - {result.stderr}"
        )
    return result.stdout


def _run_gam_json_command(args: List[str]) -> Dict[str, Any]:
    return json.loads(_run_gam_command(args))


def _build_user_info_command(email: str) -> List[str]:
    return [
        GamCommandEnum.INFO.value,
        GamCommandEnum.USER.value,
        email,
        GamCommandEnum.FORMAT_JSON.value,
    ]


def _build_user_update_json_command(email: str, filename: str) -> List[str]:
    return [
        GamCommandEnum.UPDATE.value,
        GamCommandEnum.USER.value,
        email,
        GamCommandEnum.JSON.value,
        GamCommandEnum.FILE.value,
        filename,
    ]


def _build_user_ou_command(email: str, org_unit_path: str) -> List[str]:
    return [
        GamCommandEnum.UPDATE.value,
        GamCommandEnum.USER.value,
        email,
        GamCommandEnum.OU.value,
        org_unit_path,
    ]


def _append_preview(args: List[str], preview: bool) -> List[str]:
    if preview:
        args.append(GamCommandEnum.PREVIEW.value)
    return args


def _append_operation_result(
    results: Dict[str, List[Dict[str, Any]]],
    operation: str,
    key: str,
    value: str,
    out: str,
) -> None:
    results[operation].append({key: value, "out": out})


def _parse_groups(data: Dict[str, Any]) -> List[GamUserGroup]:
    groups: List[GamUserGroup] = []
    for group in data.get(GamAttributeEnum.GROUPS.value, []):
        name = _resolve_group_name(group)
        email = _resolve_group_email(group)
        groups.append(GamUserGroup(name=name, email=email))
    return groups


def _parse_licenses(data: Dict[str, Any]) -> List[GamUserLicense]:
    licenses: List[GamUserLicense] = []
    for licence in (
        data.get(GamAttributeEnum.LICENSES.value, [])
        or data.get(GamAttributeEnum.LICENSED.value, [])
        or []
    ):
        sku_id = _resolve_license_sku_id(licence)
        sku_name = _resolve_license_sku_name(licence)
        licenses.append(GamUserLicense(sku_id=sku_id, sku_name=sku_name))
    return licenses


def _resolve_group_name(group: Dict[str, Any]) -> Any:
    return (
        group.get(GamAttributeEnum.NAME.value)
        or group.get(GamAttributeEnum.EMAIL.value)
        or group.get(GamAttributeEnum.GROUP_EMAIL.value)
    )


def _resolve_group_email(group: Dict[str, Any]) -> Any:
    return group.get(GamAttributeEnum.EMAIL.value) or group.get(
        GamAttributeEnum.GROUP_EMAIL.value
    )


def _resolve_license_sku_id(licence: Dict[str, Any]) -> Any:
    return (
        licence.get(GamAttributeEnum.SKU_ID_CAMEL.value)
        or licence.get(GamAttributeEnum.SKU.value)
        or licence.get(GamAttributeEnum.SKU_ID.value)
    )


def _resolve_license_sku_name(licence: Dict[str, Any]) -> Any:
    return (
        licence.get(GamAttributeEnum.SKU_NAME_CAMEL.value)
        or licence.get(GamAttributeEnum.PRODUCT_NAME.value)
        or licence.get(GamAttributeEnum.SKU_NAME.value)
    )


def _matches(existing, candidate) -> bool:
    try:
        if isinstance(existing, dict) and isinstance(candidate, dict):
            for key in (
                GamAttributeEnum.EMAIL.value,
                GamAttributeEnum.VALUE.value,
                GamAttributeEnum.NAME.value,
            ):
                if (
                    key in existing
                    and key in candidate
                    and existing.get(key) == candidate.get(key)
                ):
                    return True
            return existing == candidate
        return existing == candidate
    except Exception:
        return False


def _merge_user_json(
    curr: Dict[str, Any], patch: Dict[str, Any]
) -> Dict[str, Any]:
    """Merge patch into curr.

    Supports add/remove/replace for lists and shallow dict merge.
    """
    for key, value in patch.items():
        if isinstance(value, dict) and any(
            operation_key in value
            for operation_key in (
                GamAttributeEnum.ADD.value,
                GamAttributeEnum.REMOVE.value,
                GamAttributeEnum.REPLACE.value,
            )
        ):
            curr_list = curr.get(key, []) or []
            if GamAttributeEnum.REPLACE.value in value:
                curr[key] = value[GamAttributeEnum.REPLACE.value]
            else:
                if not isinstance(curr_list, list):
                    curr_list = []
                if GamAttributeEnum.ADD.value in value:
                    for item in value[GamAttributeEnum.ADD.value]:
                        if item not in curr_list:
                            curr_list.append(item)
                if GamAttributeEnum.REMOVE.value in value:
                    for item in value[GamAttributeEnum.REMOVE.value]:
                        curr_list = [
                            ci for ci in curr_list if not _matches(ci, item)
                        ]
                curr[key] = curr_list
        elif isinstance(value, list):
            curr[key] = value
        elif key in ("firstname", GamAttributeEnum.GIVEN_NAME.value):
            curr.setdefault(GamAttributeEnum.NAME.value, {})[
                GamAttributeEnum.GIVEN_NAME.value
            ] = value
        elif key in ("lastname", GamAttributeEnum.FAMILY_NAME.value):
            curr.setdefault(GamAttributeEnum.NAME.value, {})[
                GamAttributeEnum.FAMILY_NAME.value
            ] = value
        else:
            if isinstance(value, dict) and isinstance(curr.get(key), dict):
                curr[key].update(value)
            else:
                curr[key] = value
    return curr


def _normalize_update_payload(json_obj: Any) -> Dict[str, Any]:
    if isinstance(json_obj, dict):
        return {k: v for k, v in json_obj.items() if v is not None}
    if hasattr(json_obj, "model_dump"):
        return json_obj.model_dump(exclude_none=True, by_alias=True)
    if hasattr(json_obj, "dict"):
        try:
            return json_obj.dict(exclude_none=True, by_alias=True)
        except TypeError:
            return json_obj.dict(exclude_none=True)
    raise TypeError("Unsupported update payload type")


def _load_user_json(email: str) -> Dict[str, Any]:
    return _run_gam_json_command(_build_user_info_command(email))


def parse_user_json(data: Dict[str, Any]) -> GamUserDto:
    username = data.get(GamAttributeEnum.PRIMARY_EMAIL.value) or data.get(
        GamAttributeEnum.USERNAME.value
    )

    settings = GamUserSettings(
        first_name=data.get(GamAttributeEnum.NAME.value, {}).get(
            GamAttributeEnum.GIVEN_NAME.value
        ),
        last_name=data.get(GamAttributeEnum.NAME.value, {}).get(
            GamAttributeEnum.FAMILY_NAME.value
        ),
        full_name=data.get(GamAttributeEnum.NAME.value, {}).get(
            GamAttributeEnum.FULL_NAME.value
        ),
        languages=data.get(GamAttributeEnum.LANGUAGES.value),
        is_super_admin=data.get(GamAttributeEnum.IS_ADMIN.value),
        is_delegated_admin=data.get(GamAttributeEnum.IS_DELEGATED_ADMIN.value),
        two_step_enrolled=data.get(GamAttributeEnum.IS_ENROLLED_IN_2SV.value),
        two_step_enforced=data.get(GamAttributeEnum.IS_ENFORCED_IN_2SV.value),
        has_agreed_to_terms=data.get(GamAttributeEnum.AGREED_TO_TERMS.value),
        ip_whitelisted=data.get(GamAttributeEnum.IP_WHITELISTED.value),
        account_suspended=data.get(GamAttributeEnum.SUSPENDED.value),
        is_archived=data.get(GamAttributeEnum.ARCHIVED.value),
        must_change_password=data.get(
            GamAttributeEnum.CHANGE_PASSWORD_AT_NEXT_LOGIN.value
        ),
        google_unique_id=data.get(GamAttributeEnum.ID.value),
        customer_id=data.get(GamAttributeEnum.CUSTOMER_ID.value),
        mailbox_is_setup=data.get(GamAttributeEnum.IS_MAILBOX_SETUP.value),
        included_in_gal=data.get(
            GamAttributeEnum.INCLUDE_IN_GLOBAL_ADDRESS_LIST.value
        ),
        creation_time=data.get(GamAttributeEnum.CREATION_TIME.value),
        last_login_time=data.get(GamAttributeEnum.LAST_LOGIN_TIME.value),
        google_org_unit_path=data.get(GamAttributeEnum.ORG_UNIT_PATH.value),
        recovery_email=data.get(GamAttributeEnum.RECOVERY_EMAIL.value),
        photo_url=data.get(GamAttributeEnum.THUMBNAIL_PHOTO_URL.value),
    )

    groups = _parse_groups(data)
    licenses = _parse_licenses(data)

    return GamUserDto(
        username=username,
        settings=settings,
        groups=groups,
        licenses=licenses,
        raw_output=json.dumps(data),
    )


def info_user(email: str, quick: bool = False) -> GamUserDto:
    args = _build_user_info_command(email)
    if quick:
        pass
    data = _run_gam_json_command(args)
    return parse_user_json(data)


def update_user_json(
    email: str, json_obj: Any, preview: bool = False
) -> GamUserDto:
    try:
        current = _load_user_json(email)
    except Exception:
        current = {}

    merged = _merge_user_json(current, _normalize_update_payload(json_obj))
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, suffix=".json"
    ) as tf:
        json.dump(merged, tf)
        tf.flush()
        filename = tf.name

    args = _build_user_update_json_command(email, filename)
    if preview:
        _run_gam_command(_append_preview(args, preview))
        return parse_user_json(merged)

    _run_gam_command(args)
    return parse_user_json(_load_user_json(email))


def move_user_ou(
    email: str,
    org_unit_path: str,
    immutableous: Optional[str] = None,
    preview: bool = False,
) -> GamUserDto:
    args = _build_user_ou_command(email, org_unit_path)
    if immutableous:
        args += ["immutableous", immutableous]
    if preview:
        _run_gam_command(_append_preview(args, preview))
        return parse_user_json(_load_user_json(email))

    _run_gam_command(args)
    return parse_user_json(_load_user_json(email))


def update_user_groups(
    email: str,
    add: List[str] = None,
    remove: List[str] = None,
    role: Optional[str] = None,
) -> GamUserDto:
    # add: list of group emails to add; remove: list to remove
    results = {"added": [], "removed": []}
    if add:
        for g in add:
            args = [
                GamCommandEnum.UPDATE.value,
                GamCommandEnum.USER.value,
                email,
                GamCommandEnum.ADD.value,
                GamCommandEnum.GROUPS.value,
                g,
            ]
            if role:
                args += [role]
            out = _run_gam_command(args)
            _append_operation_result(
                results,
                GamAttributeEnum.ADD.value + "ed",
                GamCommandEnum.GROUP.value,
                g,
                out,
            )
    if remove:
        for g in remove:
            args = [
                GamCommandEnum.UPDATE.value,
                GamCommandEnum.USER.value,
                email,
                GamCommandEnum.REMOVE.value,
                GamCommandEnum.GROUPS.value,
                g,
            ]
            out = _run_gam_command(args)
            _append_operation_result(
                results,
                GamAttributeEnum.REMOVE.value + "d",
                GamCommandEnum.GROUP.value,
                g,
                out,
            )
    return parse_user_json(_load_user_json(email))


def manage_licenses(
    email: str, add: List[str] = None, remove: List[str] = None
) -> GamUserDto:
    results = {"added": [], "removed": []}
    if add:
        for sku in add:
            out = _run_gam_command(
                [
                    GamCommandEnum.UPDATE.value,
                    GamCommandEnum.USER.value,
                    email,
                    GamCommandEnum.LICENSE.value,
                    sku,
                ]
            )
            _append_operation_result(
                results,
                GamAttributeEnum.ADD.value + "ed",
                GamAttributeEnum.SKU.value,
                sku,
                out,
            )
    if remove:
        for sku in remove:
            out = _run_gam_command(
                [
                    GamCommandEnum.DELETE.value,
                    GamCommandEnum.LICENSE.value,
                    GamCommandEnum.USER.value,
                    email,
                    sku,
                ]
            )
            _append_operation_result(
                results,
                GamAttributeEnum.REMOVE.value + "d",
                GamAttributeEnum.SKU.value,
                sku,
                out,
            )
    return parse_user_json(_load_user_json(email))


def get_drive_quota(email: str) -> Dict[str, Any]:
    # GAM has commands related to Drive activity. Here we use info user.
    data = _run_gam_json_command(_build_user_info_command(email))
    # attempt to extract drive usage info if present
    drive = data.get("drive", {})
    return GamUserQuotaDto(drive=drive)


def suspend_user(email: str, suspend: bool = True) -> GamUserDto:
    if suspend:
        _run_gam_command(
            [GamCommandEnum.SUSPEND.value, GamCommandEnum.USER.value, email]
        )
    else:
        _run_gam_command(
            [GamCommandEnum.UNSUSPEND.value, GamCommandEnum.USER.value, email]
        )
    return parse_user_json(_load_user_json(email))
