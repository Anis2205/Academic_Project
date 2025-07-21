from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Category, Product, Review, DIY, DIYComment, UserProfile, 
    WishlistItem, VisitLog, ExternalResource, ContactMessage, Newsletter
)
from .models_stats import SiteVisitStats


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created', 'updated']
    list_filter = ['category', 'is_compostable', 'is_reusable', 'is_recyclable', 'is_biodegradable', 'is_organic', 'is_energy_efficient', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['comment', 'user__username', 'product__name']


class DIYCommentInline(admin.TabularInline):
    model = DIYComment
    extra = 0
    readonly_fields = ['user', 'comment', 'created']


@admin.register(DIY)
class DIYAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'created']
    list_filter = ['category', 'difficulty', 'created']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'materials', 'instructions']
    inlines = [DIYCommentInline]


@admin.register(DIYComment)
class DIYCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'diy', 'created']
    list_filter = ['created']
    search_fields = ['comment', 'user__username', 'diy__title']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_eco_points')
    
    def get_eco_points(self, obj):
        try:
            return obj.profile.eco_points
        except UserProfile.DoesNotExist:
            return 0
    get_eco_points.short_description = 'Eco Points'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added']
    list_filter = ['added']
    search_fields = ['user__username', 'product__name']


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'page_visited', 'timestamp', 'time_spent', 'ip_address']
    list_filter = ['timestamp', 'page_visited', 'user']
    search_fields = ['user__username', 'session_key', 'page_visited', 'ip_address']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'session_key', 'page_visited', 'timestamp', 'time_spent', 'ip_address']
    
    def has_add_permission(self, request):
        return False


@admin.register(ExternalResource)
class ExternalResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'category', 'created']
    list_filter = ['category', 'created']
    search_fields = ['title', 'description', 'url']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created', 'is_read']
    list_filter = ['is_read', 'created']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created'
    readonly_fields = ['name', 'email', 'subject', 'message', 'created']
    
    def has_add_permission(self, request):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_date', 'is_active']
    list_filter = ['is_active', 'subscribed_date']
    search_fields = ['email']
    date_hierarchy = 'subscribed_date'


@admin.register(SiteVisitStats)
class SiteVisitStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'visit_count', 'unique_visitors']
    list_filter = ['date']
    date_hierarchy = 'date'
    
    def changelist_view(self, request, extra_context=None):
        # Get today's visitors
        extra_context = extra_context or {}
        today = timezone.now().date()
        
        # Get recent visitors from VisitLog
        recent_visits = VisitLog.objects.filter(timestamp__date=today).order_by('-timestamp')[:20]
        
        # Format visitor data for display
        visitor_data = []
        for visit in recent_visits:
            if visit.user:
                visitor_type = 'User'
                identifier = visit.user.username
            else:
                visitor_type = 'Anonymous'
                identifier = visit.ip_address
            
            visitor_data.append({
                'type': visitor_type,
                'identifier': identifier,
                'page': visit.page_visited,
                'time': visit.timestamp,
            })
        
        extra_context['recent_visitors'] = visitor_data
        return super().changelist_view(request, extra_context=extra_context)


# user name : admin
# password : 123superuser