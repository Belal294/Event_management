from users.models import CustomUser

def profile_image_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile_picture') and request.user.profile_picture:
        return {'profile_picture': request.user.profile_picture.url}
    return {'profile_picture': None}
