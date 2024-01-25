from .models import Subscriber

def user_profile(request):

    if request.user.is_anonymous:
        pass

    else: 
        if request.user.is_authenticated:
            try:
                subscriber = Subscriber.objects.get(user=request.user)

                user_data = {
                    'subscriber': subscriber,
                }

                return user_data
            except(Subscriber.DoesNotExist):
                pass
    return {}

