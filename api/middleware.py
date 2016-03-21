from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class KongConsumerMiddleware(object):  
    """
    Get the user credentials from the Kong headers:

        X-Consumer-ID, the ID of the Consumer on Kong
        X-Consumer-Custom-ID, the custom_id of the Consumer (if set)
        X-Consumer-Username, the username of the Consumer (if set)
    """
    def process_request(self, request):

        # handle both possible cases:
        username = request.META.get('HTTP_X_CONSUMER_USERNAME', \
                        request.META.get('X-Consumer-Username', None))
        id = request.META.get('HTTP_X_CONSUMER_CUSTOM_ID', \
                    request.META.get('X-Consumer-Custom-ID', None))
        
        if not username is None:
            try: 
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, id=id)
            
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        return None            
            