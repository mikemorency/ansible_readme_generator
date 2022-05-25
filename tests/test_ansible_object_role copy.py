from src.classes.ansible_objects.role import Role
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
def role():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    role = Role(root_dir=f"{script_dir}/resources/test_role")
    return role

def test_role_init_failure():
    with pytest.raises(Exception):
        role = Role(root_dir="madeup")


def test_properties(role):
    assert role.name == "test_role"
    assert role.namespace == "test"
