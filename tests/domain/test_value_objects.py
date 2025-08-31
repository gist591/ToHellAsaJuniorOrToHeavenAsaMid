import pytest

from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)


def test_incident_priority_values():
    """Test incident priority enum values"""
    assert IncidentPriority.LOW.value == "low"
    assert IncidentPriority.MEDIUM.value == "medium"
    assert IncidentPriority.HIGH.value == "high"
    assert IncidentPriority.CRITICAL.value == "critical"


def test_incident_priority_comparison():
    """Test incident priority comparison"""
    assert IncidentPriority.LOW < IncidentPriority.MEDIUM
    assert IncidentPriority.MEDIUM < IncidentPriority.HIGH
    assert IncidentPriority.HIGH < IncidentPriority.CRITICAL

    assert IncidentPriority.CRITICAL > IncidentPriority.HIGH
    assert IncidentPriority.HIGH > IncidentPriority.MEDIUM
    assert IncidentPriority.MEDIUM > IncidentPriority.LOW


def test_incident_priority_from_string():
    """Test creating priority from string"""
    assert IncidentPriority.from_string("low") == IncidentPriority.LOW
    assert IncidentPriority.from_string("MEDIUM") == IncidentPriority.MEDIUM
    assert IncidentPriority.from_string("High") == IncidentPriority.HIGH
    assert IncidentPriority.from_string("CRITICAL") == IncidentPriority.CRITICAL


def test_incident_priority_from_string_invalid():
    """Test creating priority from invalid string"""
    with pytest.raises(ValueError, match="Invalid priority: invalid"):
        IncidentPriority.from_string("invalid")


def test_incident_priority_string_representation():
    """Test priority string representation"""
    assert str(IncidentPriority.LOW) == "low"
    assert str(IncidentPriority.MEDIUM) == "medium"
    assert str(IncidentPriority.HIGH) == "high"
    assert str(IncidentPriority.CRITICAL) == "critical"
