from rolepermissions.permissions import register_object_checker
from my_project.roles import SystemAdmin


@register_object_checker()
def access_clinic(role, user, clinic):
    if role == SystemAdmin:
        return True

    if user.clinic == clinic:
        return True

    return False