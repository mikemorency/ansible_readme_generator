from os import path
from .ansible_objects.role import Role
from .ansible_objects.collection import Collection


class AnsibleObjectFactory():

    def __init__(self):
        pass

    def create_object(self, root_dir: str, namespace: str = None):
        full_dir = path.abspath(root_dir)
        if path.exists(path.join(full_dir, 'meta', 'main.yml')):
            return Role(full_dir, namespace=namespace)

        elif path.exists(path.join(full_dir, 'galaxy.yml')):
            return Collection(full_dir)

        else:
            raise TypeError("Unable to determine this project's Ansible object type.")
