import time
import logging
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .models import VisitLog
from .models_stats import SiteVisitStats

logger = logging.getLogger(__name__)

class VisitLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.debug("VisitLogMiddleware initialized")
    
    def should_skip_tracking(self, path):
        """Determine if this path should be excluded from tracking"""
        excluded_paths = ['/admin', '/static/', '/media/', '/favicon.ico']
        for excluded in excluded_paths:
            if path.startswith(excluded):
                logger.debug(f"Skipping tracking for excluded path: {path}")
                return True
        return False
        
    def __call__(self, request):
        path = request.path
        logger.debug(f"Processing request for path: {path}")
        
        # Check if we should skip tracking before doing anything else
        should_skip = self.should_skip_tracking(path)
        
        # Store the start time only if we're tracking this request
        if not should_skip:
            request.visit_start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # If this is an excluded path, just return the response
        if should_skip:
            return response
            
        # Calculate time spent
        time_spent = time.time() - request.visit_start_time
        logger.debug(f"Time spent on {path}: {time_spent:.2f} seconds")
        
        try:
            # Log the visit
            if request.user.is_authenticated:
                logger.debug(f"Logging visit for authenticated user: {request.user.username}")
                VisitLog.objects.create(
                    user=request.user,
                    page_visited=path,
                    ip_address=self.get_client_ip(request),
                    time_spent=timedelta(seconds=time_spent)
                )
            elif request.session.session_key:
                logger.debug(f"Logging visit for session: {request.session.session_key}")
                VisitLog.objects.create(
                    session_key=request.session.session_key,
                    page_visited=path,
                    ip_address=self.get_client_ip(request),
                    time_spent=timedelta(seconds=time_spent)
                )
                
            # Update site-wide visit statistics
            today = timezone.now().date()
            with transaction.atomic():
                stats, created = SiteVisitStats.objects.get_or_create(date=today)
                stats.visit_count += 1
                logger.debug(f"Incrementing visit count for {today} to {stats.visit_count}")
                
                # Track unique visitors based on session key or user ID
                visitor_key = f"visitor_{today.isoformat()}"
                if request.user.is_authenticated:
                    visitor_id = f"user_{request.user.id}"
                elif request.session.session_key:
                    visitor_id = f"session_{request.session.session_key}"
                else:
                    visitor_id = f"ip_{self.get_client_ip(request)}"
                
                cookie_name = f"visitor_counted_{visitor_id}"
                if not request.COOKIES.get(cookie_name):
                    stats.unique_visitors += 1
                    logger.debug(f"Incrementing unique visitors to {stats.unique_visitors} for {visitor_id}")
                    response.set_cookie(cookie_name, 'yes', max_age=86400)  # 24 hours
                
                stats.save()
        except Exception as e:
            logger.error(f"Error in VisitLogMiddleware: {e}")
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip