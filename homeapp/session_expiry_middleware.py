from django.shortcuts import redirect
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class SessionExpiryMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'is_created' in request.session:
            session_created_time = request.session['is_created']
            
            if session_created_time:
                session_created_time = timezone.make_aware(
                    timezone.datetime.strptime(session_created_time, '%Y-%m-%d %H:%M:%S.%f%z')
                )
                session_age = timezone.now() - session_created_time

                # Set timeout to expire after one hour
                if session_age.total_seconds() > 3600: 
                    request.session.flush()  # Clear session data
                    return redirect('login')

        return None