
import pytest

from data_onboarding.acl.paths import (
    normalize_channel,
    normalize_path,
    normalize_project_key,
    path_has_prefix,
)


def test_normalize_path_basic():
    assert normalize_path("/SharePoint/Legal/Contracts/x.pdf") == "/SharePoint/Legal/Contracts/x.pdf"
    assert normalize_path("\\SharePoint\\Legal\\Contracts\\x.pdf") == "/SharePoint/Legal/Contracts/x.pdf"
    assert normalize_path("/SharePoint//Legal/./Contracts/x.pdf") == "/SharePoint/Legal/Contracts/x.pdf"

def test_normalize_path_traversal():
    assert (
        normalize_path("/SharePoint/Public/SOPs/../../Legal/Contracts/x.pdf")
        == "/SharePoint/Legal/Contracts/x.pdf"
    )

def test_normalize_path_climb_above_root_raises():
    with pytest.raises(ValueError, match="climbs above root"):
        normalize_path("/SharePoint/../../x.pdf")

def test_normalize_path_null_byte_raises():
    with pytest.raises(ValueError, match='Null byte'):
        normalize_path("/SharePoint/Legal/\x00x.pdf")

def test_path_has_prefix_segment_boundary():
    assert path_has_prefix(
        "/SharePoint/Legal/Contracts/x.pdf",
        "/SharePoint/Legal/Contracts/",
    )

    assert not path_has_prefix(
        "/sharepoint/legal/contracts/x.pdf",
        "/SharePoint/Legal/Contracts/",
    )

    assert not path_has_prefix(
        "/SharePoint/Legal/Contracts-archive/x.pdf",
        "/SharePoint/Legal/Contracts/",
    )

def test_normalize_channel_and_project():
    assert normalize_channel(" #General ") == "general"
    assert normalize_channel("announcements") == "announcements"
    assert normalize_project_key(" WH ") == "WH"


