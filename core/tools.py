from django.contrib.auth import get_user_model
from core.models import Organization


def authenticate(email=None, organiz=None, password=None):
    user_model = get_user_model()
    try:
        user = user_model.objects.get(email=email)
        organization = Organization.objects.get(name=organiz)
    except (user_model.DoesNotExist, Organization.DoesNotExist):
        return None

    else:
        if hasattr(user, "profile"):
            if organization in user.profile.organization.all():
                if user.check_password(password):
                    user.profile.organiz_login = organization
                    user.profile.save()
                    return user
    return None
