from users.models import CustomUser

def profile_image_context(request):
    if request.user.is_authenticated:
        return {'profile_image': request.user.profile_image}
    return {'profile_image': None}
