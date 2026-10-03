"""Opt-in experimental anatomy: explicit authority and artifact roles."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator
import pytest

ROOT = Path(__file__).resolve().parents[1]


def validator():
    return Draft202012Validator(json.loads((ROOT / 'schemas/project-structure-profile-1.schema.json').read_text()))


def test_declared_semantic_project_profile():
    profile = json.loads((ROOT / 'profiles/semantic-project.json').read_text())
    validator().validate(profile)
    assert set(profile['artifact_classes']) == {'authoritative', 'derived', 'mixed', 'interpretation'}
    assert 'src/' not in profile['required_paths']


@pytest.mark.parametrize('field,value', [('schema_version','future'),('artifact_classes',['automatic-authority']),('required_paths',42)])
def test_unknown_or_malformed_profile_refuses(field, value):
    profile = json.loads((ROOT / 'profiles/semantic-project.json').read_text())
    profile[field] = value
    assert list(validator().iter_errors(profile))
