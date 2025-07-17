from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import (
    Product, Category, Review, DIY, DIYComment, UserProfile, 
    WishlistItem, VisitLog, ExternalResource, ContactMessage, Newsletter
)
from .forms import (
    ReviewForm, ProductSearchForm, DIYForm, DIYCommentForm, DIYSearchForm,
    UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm,
    CustomPasswordResetForm, CustomSetPasswordForm, ContactForm, NewsletterForm,
    GlobalSearchForm
)


# Home view
class HomeView(TemplateView):
    """Home page view"""
    template_name = 'greenapp/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:6]
        context['latest_diy'] = DIY.objects.all()[:3]
        context['newsletter_form'] = NewsletterForm()
        return context


# Product views
class ProductListView(ListView):
    """View for displaying all products with search and filter options"""
    model = Product
    template_name = 'greenapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.all()
        form = ProductSearchForm(self.request.GET)
        
        if form.is_valid():
            # Apply search query
            query = form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | 
                    Q(description__icontains=query)
                )
            
            # Apply category filter
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            # Apply price range filter
            min_price = form.cleaned_data.get('min_price')
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
                
            max_price = form.cleaned_data.get('max_price')
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            # Apply sustainability filters
            for field in ['is_compostable', 'is_reusable', 'is_recyclable', 
                         'is_biodegradable', 'is_organic', 'is_energy_efficient']:
                value = form.cleaned_data.get(field)
                if value:
                    queryset = queryset.filter(**{field: True})
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """View for displaying product details"""
    model = Product
    template_name = 'greenapp/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['reviews'] = self.object.reviews.all()
        
        # Check if product is in user's wishlist
        if self.request.user.is_authenticated:
            context['in_wishlist'] = WishlistItem.objects.filter(
                user=self.request.user, 
                product=self.object
            ).exists()
        
        # Get related products
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        
        # Log visit
        if self.request.user.is_authenticated:
            VisitLog.objects.create(
                user=self.request.user,
                page_visited=f'Product: {self.object.name}',
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
        elif self.request.session.session_key:
            VisitLog.objects.create(
                session_key=self.request.session.session_key,
                page_visited=f'Product: {self.object.name}',
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
        
        return context


class CategoryDetailView(ListView):
    """View for displaying products by category"""
    model = Product
    template_name = 'greenapp/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """View for creating product reviews"""
    model = Review
    form_class = ReviewForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = get_object_or_404(Product, slug=self.kwargs['slug'])
        
        # Check if user already reviewed this product
        existing_review = Review.objects.filter(
            user=self.request.user,
            product=form.instance.product
        ).first()
        
        if existing_review:
            messages.error(self.request, "You have already reviewed this product.")
            return redirect('product_detail', slug=self.kwargs['slug'])
        
        messages.success(self.request, "Your review has been added successfully!")
        
        # Award eco points to the user
        self.request.user.profile.eco_points += 5
        self.request.user.profile.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('product_detail', kwargs={'slug': self.kwargs['slug']})


# DIY views
class DIYListView(ListView):
    """View for displaying all DIY tutorials"""
    model = DIY
    template_name = 'greenapp/diy_list.html'
    context_object_name = 'tutorials'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = DIY.objects.all()
        form = DIYSearchForm(self.request.GET)
        
        if form.is_valid():
            # Apply search query
            query = form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(materials__icontains=query) |
                    Q(instructions__icontains=query)
                )
            
            # Apply category filter
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            # Apply difficulty filter
            difficulty = form.cleaned_data.get('difficulty')
            if difficulty:
                queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DIYSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


class DIYDetailView(DetailView):
    """View for displaying DIY tutorial details"""
    model = DIY
    template_name = 'greenapp/diy_detail.html'
    context_object_name = 'tutorial'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = DIYCommentForm()
        context['comments'] = self.object.comments.all()
        
        # Get related tutorials
        if self.object.category:
            context['related_tutorials'] = DIY.objects.filter(
                category=self.object.category
            ).exclude(id=self.object.id)[:3]
        else:
            context['related_tutorials'] = DIY.objects.exclude(id=self.object.id)[:3]
        
        # Log visit
        if self.request.user.is_authenticated:
            VisitLog.objects.create(
                user=self.request.user,
                page_visited=f'DIY: {self.object.title}',
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
        elif self.request.session.session_key:
            VisitLog.objects.create(
                session_key=self.request.session.session_key,
                page_visited=f'DIY: {self.object.title}',
                ip_address=self.request.META.get('REMOTE_ADDR')
            )
        
        return context


class DIYCreateView(LoginRequiredMixin, CreateView):
    """View for creating new DIY tutorials"""
    model = DIY
    form_class = DIYForm
    template_name = 'greenapp/diy_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your DIY tutorial has been created successfully!")
        
        # Award eco points to the user
        self.request.user.profile.eco_points += 10
        self.request.user.profile.save()
        
        return super().form_valid(form)


class DIYUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating DIY tutorials"""
    model = DIY
    form_class = DIYForm
    template_name = 'greenapp/diy_form.html'
    
    def test_func(self):
        tutorial = self.get_object()
        return self.request.user == tutorial.author
    
    def form_valid(self, form):
        messages.success(self.request, "Your DIY tutorial has been updated successfully!")
        return super().form_valid(form)


class DIYDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting DIY tutorials"""
    model = DIY
    template_name = 'greenapp/diy_confirm_delete.html'
    success_url = reverse_lazy('diy_list')
    
    def test_func(self):
        tutorial = self.get_object()
        return self.request.user == tutorial.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your DIY tutorial has been deleted.")
        return super().delete(request, *args, **kwargs)


class DIYCommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating comments on DIY tutorials"""
    model = DIYComment
    form_class = DIYCommentForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.diy = get_object_or_404(DIY, slug=self.kwargs['slug'])
        messages.success(self.request, "Your comment has been added successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('diy_detail', kwargs={'slug': self.kwargs['slug']})


# User views
class UserRegistrationView(SuccessMessageMixin, CreateView):
    """View for user registration"""
    form_class = UserRegistrationForm
    template_name = 'greenapp/register.html'
    success_url = reverse_lazy('login')
    success_message = "Your account has been created successfully! You can now log in."


class UserLoginView(SuccessMessageMixin, LoginView):
    """Custom login view with form styling"""
    form_class = UserLoginForm
    template_name = 'greenapp/login.html'
    success_message = "You have successfully logged in."


class UserLogoutView(LogoutView):
    """Custom logout view"""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, DetailView):
    """View for displaying user profile"""
    model = User
    template_name = 'greenapp/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        username = self.kwargs.get('username')
        if username:
            return get_object_or_404(User, username=username)
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        context['reviews'] = Review.objects.filter(user=user).order_by('-created')[:5]
        context['diy_tutorials'] = DIY.objects.filter(author=user).order_by('-created')[:5]
        context['wishlist_items'] = WishlistItem.objects.filter(user=user).order_by('-added')[:5]
        
        # Only show visit history to the profile owner
        if user == self.request.user:
            context['visit_logs'] = VisitLog.objects.filter(user=user).order_by('-timestamp')[:10]
        
        return context


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating user profile"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'greenapp/profile_update.html'
    success_message = "Your profile has been updated successfully."
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        
        if user_form.is_valid():
            user_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('profile')


class UserWishlistView(LoginRequiredMixin, ListView):
    """View for displaying user's wishlist"""
    model = WishlistItem
    template_name = 'greenapp/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 10
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).order_by('-added')


class UserReviewsView(LoginRequiredMixin, ListView):
    """View for displaying user's reviews"""
    model = Review
    template_name = 'greenapp/reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created')


class UserDIYTutorialsView(LoginRequiredMixin, ListView):
    """View for displaying user's DIY tutorials"""
    model = DIY
    template_name = 'greenapp/diy_tutorials.html'
    context_object_name = 'tutorials'
    paginate_by = 10
    
    def get_queryset(self):
        return DIY.objects.filter(author=self.request.user).order_by('-created')


class UserHistoryView(LoginRequiredMixin, ListView):
    """View for displaying user's visit history"""
    model = VisitLog
    template_name = 'greenapp/history.html'
    context_object_name = 'visit_logs'
    paginate_by = 20
    
    def get_queryset(self):
        return VisitLog.objects.filter(user=self.request.user).order_by('-timestamp')


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with form styling"""
    form_class = CustomPasswordResetForm
    template_name = 'greenapp/password_reset.html'
    email_template_name = 'greenapp/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view with form styling"""
    form_class = CustomSetPasswordForm
    template_name = 'greenapp/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UserDashboardView(LoginRequiredMixin, TemplateView):
    """View for user dashboard with summary of activities"""
    template_name = 'greenapp/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get counts
        context['review_count'] = Review.objects.filter(user=user).count()
        context['diy_count'] = DIY.objects.filter(author=user).count()
        context['wishlist_count'] = WishlistItem.objects.filter(user=user).count()
        
        # Get recent activity
        context['recent_reviews'] = Review.objects.filter(user=user).order_by('-created')[:3]
        context['recent_diy'] = DIY.objects.filter(author=user).order_by('-created')[:3]
        context['recent_wishlist'] = WishlistItem.objects.filter(user=user).order_by('-added')[:3]
        
        # Get visit statistics
        one_month_ago = timezone.now() - timedelta(days=30)
        context['visit_count'] = VisitLog.objects.filter(user=user).count()
        context['recent_visits'] = VisitLog.objects.filter(
            user=user, 
            timestamp__gte=one_month_ago
        ).count()
        
        return context


# Wishlist views
def toggle_wishlist(request, product_id):
    """View for adding/removing products from wishlist"""
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your wishlist.")
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        # Remove from wishlist
        wishlist_item.delete()
        messages.success(request, f"{product.name} has been removed from your wishlist.")
    else:
        # Add to wishlist
        WishlistItem.objects.create(user=request.user, product=product)
        messages.success(request, f"{product.name} has been added to your wishlist.")
    
    # Redirect back to the referring page
    next_url = request.GET.get('next', 'product_list')
    return redirect(next_url)


# External resources view
class ExternalResourceListView(ListView):
    """View for displaying external eco-friendly resources"""
    model = ExternalResource
    template_name = 'greenapp/external_resources.html'
    context_object_name = 'resources'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = ExternalResource.objects.all()
        category_id = self.request.GET.get('category')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# Contact and about views
class ContactView(SuccessMessageMixin, CreateView):
    """View for contact form"""
    model = ContactMessage
    form_class = ContactForm
    template_name = 'greenapp/contact.html'
    success_url = reverse_lazy('contact')
    success_message = "Your message has been sent successfully! We'll get back to you soon."


class AboutView(TemplateView):
    """View for about page"""
    template_name = 'greenapp/about.html'


# Newsletter subscription
def newsletter_subscribe(request):
    """View for newsletter subscription"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email already exists
            if Newsletter.objects.filter(email=email).exists():
                messages.info(request, "You are already subscribed to our newsletter.")
            else:
                form.save()
                messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "Please enter a valid email address.")
    
    return redirect('home')


# Search view
class SearchView(ListView):
    """View for global search across products and DIY tutorials"""
    template_name = 'greenapp/search_results.html'
    context_object_name = 'results'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            # Search in products
            product_results = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
            
            # Search in DIY tutorials
            diy_results = DIY.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(materials__icontains=query) |
                Q(instructions__icontains=query)
            )
            
            # Combine results
            self.product_count = product_results.count()
            self.diy_count = diy_results.count()
            
            # Return combined results
            return list(product_results) + list(diy_results)
        return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['product_count'] = getattr(self, 'product_count', 0)
        context['diy_count'] = getattr(self, 'diy_count', 0)
        context['total_count'] = context['product_count'] + context['diy_count']
        return context