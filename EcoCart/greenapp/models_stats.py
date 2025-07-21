from django.db import models
from django.utils import timezone

class SiteVisitStats(models.Model):
    """Model to track site-wide visit statistics"""
    date = models.DateField(unique=True, default=timezone.now)
    visit_count = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Site Visit Statistic'
        verbose_name_plural = 'Site Visit Statistics'
    
    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.visit_count} visits"