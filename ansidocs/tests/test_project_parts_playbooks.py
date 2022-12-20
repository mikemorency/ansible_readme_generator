from ansidocs.src.classes.project_parts.playbooks import Playbooks
import pytest
import os

# with mock.patch('yourmodule.isdir') as mocked_isdir, \
#         mock.patch('yourmodule.listdir') as mocked_listdir:
#     mocked_isdir.return_value = True
#     mocked_listdir.return_value = ['filename1', 'filename2']

#     yourmodule.foo('/spam/eggs')

#     mocked_isdir.assert_called_with('/spam/eggs/baz/foo')
#     mocked_listdir.assert_called_with('/spam/eggs/baz/foo')

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
