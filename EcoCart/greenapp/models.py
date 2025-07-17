from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """Model for product categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class Product(models.Model):
    """Model for eco-friendly products"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    is_compostable = models.BooleanField(default=False)
    is_reusable = models.BooleanField(default=False)
    is_recyclable = models.BooleanField(default=False)
    is_biodegradable = models.BooleanField(default=False)
    is_organic = models.BooleanField(default=False)
    is_energy_efficient = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class Review(models.Model):
    """Model for product reviews"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        # Ensure a user can only review a product once
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_review')
        ]
    
    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'


class DIY(models.Model):
    """Model for DIY eco-friendly tutorials"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diy_tutorials')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='diy_tutorials')
    description = models.TextField()
    materials = models.TextField(help_text="List the materials needed for this DIY project")
    instructions = models.TextField(help_text="Step-by-step instructions for the DIY project")
    image = models.ImageField(upload_to='diy/%Y/%m/%d', blank=True)
    document = models.FileField(upload_to='diy/documents/%Y/%m/%d', blank=True)
    difficulty = models.CharField(max_length=10, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], default='medium')
    time_required = models.CharField(max_length=100, help_text="Estimated time to complete (e.g., '30 minutes', '2 hours')")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'DIY Tutorial'
        verbose_name_plural = 'DIY Tutorials'
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('diy_detail', args=[self.slug])


class DIYComment(models.Model):
    """Model for comments on DIY tutorials"""
    diy = models.ForeignKey(DIY, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diy_comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.diy.title}'


class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    location = models.CharField(max_length=100, blank=True)
    eco_points = models.IntegerField(default=0, help_text="Points earned for eco-friendly activities")
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    @property
    def total_reviews(self):
        return self.user.reviews.count()
    
    @property
    def total_diy_tutorials(self):
        return self.user.diy_tutorials.count()
    
    @property
    def total_wishlist_items(self):
        return self.user.wishlist.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    instance.profile.save()


class WishlistItem(models.Model):
    """Model for user wishlist items"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_wishlists')
    added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added']
        # Ensure a product is only in a user's wishlist once
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_wishlist_item')
        ]
    
    def __str__(self):
        return f'{self.product.name} in {self.user.username}\'s wishlist'


class VisitLog(models.Model):
    """Model to track user visits and page views"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits', null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    page_visited = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} visited {self.page_visited}"
        return f"Anonymous visited {self.page_visited}"


class ExternalResource(models.Model):
    """Model for external eco-friendly resources and websites"""
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"


class Newsletter(models.Model):
    """Model for newsletter subscriptions"""
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email