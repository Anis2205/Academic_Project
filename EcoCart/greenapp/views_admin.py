from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import json
from datetime import timedelta
from .models import VisitLog
from .models_stats import SiteVisitStats

@staff_member_required
def visitor_analytics(request):
    """Admin view for detailed visitor analytics"""
    today = timezone.now().date()
    
    # Get today's stats
    try:
        today_stats = SiteVisitStats.objects.get(date=today)
    except SiteVisitStats.DoesNotExist:
        today_stats = SiteVisitStats(date=today)
    
    # Get recent visitors
    recent_visits = VisitLog.objects.all().order_by('-timestamp')[:50]
    
    # Get top pages
    top_pages = VisitLog.objects.values('page_visited').annotate(
        count=Count('page_visited')
    ).order_by('-count')[:10]
    
    # Get top users
    top_users = VisitLog.objects.exclude(user=None).values(
        'user__username'
    ).annotate(count=Count('user')).order_by('-count')[:10]
    
    # Get top IPs
    top_ips = VisitLog.objects.values('ip_address').annotate(
        count=Count('ip_address')
    ).order_by('-count')[:10]
    
    context = {
        'today_stats': today_stats,
        'recent_visits': recent_visits,
        'top_pages': top_pages,
        'top_users': top_users,
        'top_ips': top_ips,
        'title': 'Visitor Analytics'
    }
    
    return render(request, 'admin/greenapp/analytics.html', context)


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Admin dashboard view with visitor statistics"""
    template_name = 'greenapp/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Get today's stats
        try:
            today_stats = SiteVisitStats.objects.get(date=today)
            context['today_visits'] = today_stats.visit_count
            context['today_unique'] = today_stats.unique_visitors
        except SiteVisitStats.DoesNotExist:
            context['today_visits'] = 0
            context['today_unique'] = 0
        
        # Get yesterday's stats
        try:
            yesterday_stats = SiteVisitStats.objects.get(date=yesterday)
            context['yesterday_visits'] = yesterday_stats.visit_count
        except SiteVisitStats.DoesNotExist:
            context['yesterday_visits'] = 0
        
        # Get weekly stats
        weekly_stats = SiteVisitStats.objects.filter(date__gte=week_ago)
        context['weekly_visits'] = sum(stat.visit_count for stat in weekly_stats)
        context['weekly_unique'] = sum(stat.unique_visitors for stat in weekly_stats)
        
        # Get monthly stats
        monthly_stats = SiteVisitStats.objects.filter(date__gte=month_ago)
        context['monthly_visits'] = sum(stat.visit_count for stat in monthly_stats)
        context['monthly_unique'] = sum(stat.unique_visitors for stat in monthly_stats)
        
        # Get chart data for last 30 days
        chart_data = SiteVisitStats.objects.filter(date__gte=month_ago).order_by('date')
        chart_dates = [stat.date.strftime('%b %d') for stat in chart_data]
        chart_visits = [stat.visit_count for stat in chart_data]
        chart_unique = [stat.unique_visitors for stat in chart_data]
        
        context['chart_dates'] = json.dumps(chart_dates)
        context['chart_visits'] = json.dumps(chart_visits)
        context['chart_unique'] = json.dumps(chart_unique)
        
        # Get popular pages
        context['popular_pages'] = VisitLog.objects.values('page_visited').annotate(
            count=Count('page_visited')
        ).order_by('-count')[:5]
        
        # Get recent visits - only most recent visit per unique user
        recent_visits = []
        seen_users = set()
        
        # Get visits with users first, then anonymous visits
        for visit in VisitLog.objects.filter(user__isnull=False).order_by('-timestamp'):
            if visit.user.id not in seen_users:
                recent_visits.append(visit)
                seen_users.add(visit.user.id)
                
        # Then add anonymous visits identified by IP
        if len(recent_visits) < 8:
            for visit in VisitLog.objects.filter(user__isnull=True).exclude(ip_address='').order_by('-timestamp'):
                if visit.ip_address and f"ip_{visit.ip_address}" not in seen_users:
                    recent_visits.append(visit)
                    seen_users.add(f"ip_{visit.ip_address}")
                    
                # Stop after we have 8 unique visitors
                if len(recent_visits) >= 8:
                    break
                
        context['recent_visits'] = recent_visits
        
        return context