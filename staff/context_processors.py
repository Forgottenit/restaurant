from .views import is_staffteam_or_admin


def staff_permissions(request):
    return {'is_staffteam_or_admin': is_staffteam_or_admin(request.user)}
