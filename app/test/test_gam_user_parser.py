from app.service.gam.utils.gam_user_utils import (
    parse_user_json,
    _parse_groups,
    _parse_licenses,
    _matches,
    _merge_user_json,
    _normalize_update_payload
)
from app.domain.dtos.gam import GamUserUpdateDto


class TestParseUserJson:
    """Tests for parse_user_json function."""

    def test_parse_user_json_basic(self):
        sample = {
            "primaryEmail": "user@domain.com",
            "name": {
                "givenName": "Test",
                "familyName": "User",
                "fullName": "Test User"
            },
            "isAdmin": False,
            "suspended": False,
            "groups": [{"email": "group1@domain.com", "name": "Group 1"}],
            "licenses": [{"skuId": "101", "skuName": "Workspace"}]
        }
        dto = parse_user_json(sample)
        assert dto.username == "user@domain.com"
        assert dto.settings.first_name == "Test"
        assert dto.settings.last_name == "User"
        assert len(dto.groups) == 1
        assert dto.groups[0].email == "group1@domain.com"
        assert len(dto.licenses) == 1

    def test_parse_user_json_no_groups(self):
        sample = {
            "primaryEmail": "nogroup@domain.com",
            "name": {
                "givenName": "No",
                "familyName": "Group"
            }
        }
        dto = parse_user_json(sample)
        assert dto.username == "nogroup@domain.com"
        assert dto.groups == []

    def test_parse_user_json_multiple_licenses(self):
        sample = {
            "primaryEmail": "multi@domain.com",
            "licenses": [
                {"skuId": "101", "skuName": "A"},
                {"skuId": "202", "skuName": "B"}
            ]
        }
        dto = parse_user_json(sample)
        assert len(dto.licenses) == 2


class TestParseGroups:
    """Tests for _parse_groups helper."""

    def test_parse_groups_empty(self):
        result = _parse_groups({})
        assert result == []

    def test_parse_groups_with_name(self):
        data = {"groups": [{"name": "Admins", "email": "admins@domain.com"}]}
        result = _parse_groups(data)
        assert len(result) == 1
        assert result[0].name == "Admins"


class TestParseLicenses:
    """Tests for _parse_licenses helper."""

    def test_parse_licenses_empty(self):
        result = _parse_licenses({})
        assert result == []

    def test_parse_licenses_standard(self):
        data = {"licenses": [{"skuId": "SKU123", "skuName": "Workspace Plus"}]}
        result = _parse_licenses(data)
        assert len(result) == 1
        assert result[0].sku_id == "SKU123"


class TestMatches:
    """Tests for _matches comparison helper."""

    def test_matches_same_string(self):
        assert _matches("item1", "item1") is True

    def test_matches_different_string(self):
        assert _matches("item1", "item2") is False

    def test_matches_dicts_by_email(self):
        existing = {"email": "user@domain.com", "name": "User"}
        candidate = {"email": "user@domain.com", "id": "123"}
        assert _matches(existing, candidate) is True


class TestMergeUserJson:
    """Tests for _merge_user_json intelligent merge."""

    def test_merge_scalar_replacement(self):
        curr = {"firstname": "John", "lastname": "Doe"}
        patch = {"firstname": "Jane"}
        result = _merge_user_json(curr, patch)
        # firstname maps to name.givenName
        assert result["name"]["givenName"] == "Jane"
        assert result["lastname"] == "Doe"

    def test_merge_with_add_list(self):
        curr = {"phones": [{"value": "111-1111"}]}
        patch = {"phones": {"add": [{"value": "222-2222"}]}}
        result = _merge_user_json(curr, patch)
        assert len(result["phones"]) == 2

    def test_merge_with_remove_list(self):
        curr = {
            "emails": [
                {"email": "old@domain.com"},
                {"email": "keep@domain.com"}
            ]
        }
        patch = {"emails": {"remove": [{"email": "old@domain.com"}]}}
        result = _merge_user_json(curr, patch)
        assert len(result["emails"]) == 1
        assert result["emails"][0]["email"] == "keep@domain.com"

    def test_merge_with_replace_list(self):
        curr = {"groups": [{"email": "old@domain.com"}]}
        patch = {"groups": {"replace": [{"email": "new@domain.com"}]}}
        result = _merge_user_json(curr, patch)
        assert len(result["groups"]) == 1
        assert result["groups"][0]["email"] == "new@domain.com"


class TestNormalizeUpdatePayload:
    """Tests for DTO normalization before merge."""

    def test_normalize_update_payload_excludes_nulls(self):
        payload = GamUserUpdateDto(
            firstname="Ana",
            lastname=None,
            recovery_email=None
        )
        result = _normalize_update_payload(payload)
        assert result == {"firstname": "Ana"}

    def test_normalize_update_payload_keeps_dynamic_fields(self):
        payload = GamUserUpdateDto(firstname="Ana", phones={
            "add": [
                {"value": "555-1234"}
            ]})
        result = _normalize_update_payload(payload)
        assert result["firstname"] == "Ana"
        assert result["phones"] == {"add": [{"value": "555-1234"}]}
