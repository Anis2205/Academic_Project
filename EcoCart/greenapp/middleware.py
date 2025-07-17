import time
from datetime import timedelta
from .models import VisitLog

class VisitLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Store the start time
        request.visit_start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Skip admin, static, media, and favicon requests
        if any(x in request.path for x in ['/admin/', '/static/', '/media/', '/favicon.ico']):
            return response
        
        # Calculate time spent
        time_spent = time.time() - request.visit_start_time
        
        # Log the visit
        if request.user.is_authenticated:
            VisitLog.objects.create(
                user=request.user,
                page_visited=request.path,
                ip_address=self.get_client_ip(request),
                time_spent=timedelta(seconds=time_spent)
            )
        elif request.session.session_key:
            VisitLog.objects.create(
                session_key=request.session.session_key,
                page_visited=request.path,
                ip_address=self.get_client_ip(request),
                time_spent=timedelta(seconds=time_spent)
            )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip