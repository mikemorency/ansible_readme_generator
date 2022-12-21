from src.ansidocs.classes.project_parts.playbooks import Playbooks
import pytest
import os


@pytest.fixture(scope="session")
def playbooks():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    playbooks = Playbooks(root_dir=f"{script_dir}/resources/test_collection/playbooks")
    return playbooks


def test_get_content(playbooks):
    contents = playbooks.get_content()
    assert len(contents.playbooks) == 2
    assert len(contents.subdirs) == 2
    assert contents.subdirs['subplays2'].subdirs['subplays21'].playbooks[0] == 'subplay211.yml'
