from django.shortcuts import redirect
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class SessionExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'id' in request.session and 'is_created' in request.session:
            session_created = request.session.get('is_created')
            if session_created:
                session_created_time = timezone.make_aware(timezone.datetime.strptime(session_created, '%Y-%m-%d %H:%M:%S.%f%z'))
                session_age = timezone.now() - session_created_time
                if session_age.total_seconds() > 60:  # Check if session is older than 1 minute
                    request.session.flush()  # Clear session data
                    return redirect('login')
        return None
