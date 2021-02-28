from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin or request.user.is_superuser))


class IsOwnerProject(BasePermission):
    message = 'Not allow resource'

    def has_object_permission(self, request, view, project):
        try:
            if project.company.id != request.user.company.id:
                return False
        except Exception as e:
            return False
        return True
