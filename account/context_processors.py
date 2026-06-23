def app_access_permissions(request):
    user = request.user
    if user.is_authenticated:
        return {
            "can_access_diarylab": user.is_superuser
            or user.groups.filter(name="diarylab_access").exists(),
            "can_access_comptas": user.is_superuser
            or user.groups.filter(name="comptas_access").exists(),
            "can_access_potionrun": user.is_superuser
            or user.groups.filter(name="potionrun_access").exists(),
            "can_access_escapevault": user.is_superuser
            or user.groups.filter(name="escapevault_access").exists(),
            "can_access_sami": user.is_superuser
            or user.groups.filter(name="sami_access").exists(),
        }
    return {}
