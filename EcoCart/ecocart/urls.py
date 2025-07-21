"""
URL configuration for ecocart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from greenapp import views
from django.contrib.auth import views as auth_views
from greenapp.views_admin import visitor_analytics, AdminDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/<slug:slug>/review/', views.ReviewCreateView.as_view(), name='add_review'),
    
    # DIY URLs
    path('diy/', views.DIYListView.as_view(), name='diy_list'),
    path('diy/new/', views.DIYCreateView.as_view(), name='diy_create'),
    path('diy/<slug:slug>/edit/', views.DIYUpdateView.as_view(), name='diy_update'),
    path('diy/<slug:slug>/delete/', views.DIYDeleteView.as_view(), name='diy_delete'),
    path('diy/<slug:slug>/comment/', views.DIYCommentCreateView.as_view(), name='add_diy_comment'),
    path('diy/<slug:slug>/', views.DIYDetailView.as_view(), name='diy_detail'),
    
    # User URLs
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('wishlist/', views.UserWishlistView.as_view(), name='wishlist'),
    path('my-reviews/', views.UserReviewsView.as_view(), name='my_reviews'),
    path('my-tutorials/', views.UserDIYTutorialsView.as_view(), name='my_tutorials'),
    path('history/', views.UserHistoryView.as_view(), name='history'),
    
    # Wishlist URLs
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    
    # Password reset URLs
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='greenapp/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='greenapp/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # External resources
    path('resources/', views.ExternalResourceListView.as_view(), name='external_resources'),
    
    # Contact and about
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Newsletter
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Admin dashboard
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('analytics/', visitor_analytics, name='visitor_analytics'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
