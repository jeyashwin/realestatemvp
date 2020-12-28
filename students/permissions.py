from rest_framework.permissions import BasePermission

class IsStudentUserAccess(BasePermission):
    """checking weather student user is accessing"""
    message = 'Only students can access'

    def has_permission(self, request, view):
        try:
            return request.user.usertype.is_student
        except:
            return False


class IsOwnerOfTheObject(BasePermission):
    """checking weather student user is owner of this object"""
    message = 'You cannot update this! Sorry'

    def has_object_permission(self, request, view, obj):
        return obj.student.user.user == request.user