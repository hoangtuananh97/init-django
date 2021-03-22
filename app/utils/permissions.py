from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if not hasattr(view, 'permission_code') or not view.permission_code:
            return False
        permission_code = view.permission_code
        if not request.user.has_perm(permission_code):
            return False

        return True
        # permission_code = request.META.get("HTTP_PERMISSION_CODE", None)
        # if permission_code:
        #     permissions = request.user.get_group_permissions()
        #     if permission_code in permissions:
        #         return True


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
