from src.classes.ansible_objects.collection import Collection
import pytest

# with mock.patch('yourmodule.isdir') as mocked_isdir, \
#         mock.patch('yourmodule.listdir') as mocked_listdir:
#     mocked_isdir.return_value = True
#     mocked_listdir.return_value = ['filename1', 'filename2']

#     yourmodule.foo('/spam/eggs')

#     mocked_isdir.assert_called_with('/spam/eggs/baz/foo')
#     mocked_listdir.assert_called_with('/spam/eggs/baz/foo')

@pytest.fixture(scope="session")
def collection():
    collection = Collection(root_dir="./resources/test_collection")
    return collection

def test_role_init_failure():
    with pytest.raises(Exception):
        collection = Collection(root_dir="madeup")


def test_properties(collection):
    assert collection.name == "collection"
    assert collection.namespace == "test"
