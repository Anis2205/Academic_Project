from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import (
    Review, Product, Category, DIY, DIYComment, UserProfile, 
    ContactMessage, Newsletter
)


class ReviewForm(forms.ModelForm):
    """Form for submitting product reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts about this product...', 'class': 'form-control'}),
        }


class ProductSearchForm(forms.Form):
    """Form for searching products"""
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search for eco-friendly products...', 'class': 'form-control'}
    ))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price', 'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price', 'class': 'form-control'})
    )
    
    # Sustainability filters
    is_compostable = forms.BooleanField(required=False)
    is_reusable = forms.BooleanField(required=False)
    is_recyclable = forms.BooleanField(required=False)
    is_biodegradable = forms.BooleanField(required=False)
    is_organic = forms.BooleanField(required=False)
    is_energy_efficient = forms.BooleanField(required=False)


class DIYForm(forms.ModelForm):
    """Form for creating and updating DIY tutorials"""
    class Meta:
        model = DIY
        fields = ['title', 'category', 'description', 'materials', 'instructions', 
                 'image', 'document', 'difficulty', 'time_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'materials': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'time_required': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class DIYCommentForm(forms.ModelForm):
    """Form for commenting on DIY tutorials"""
    class Meta:
        model = DIYComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Share your thoughts or ask questions about this DIY tutorial...',
                'class': 'form-control'
            }),
        }


class DIYSearchForm(forms.Form):
    """Form for searching DIY tutorials"""
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search for DIY tutorials...', 'class': 'form-control'}
    ))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Any Difficulty'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UserLoginForm(AuthenticationForm):
    """Custom login form with styled fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with styled fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with styled fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }
        labels = {
            'email': '',
        }


class GlobalSearchForm(forms.Form):
    """Form for global search across the site"""
    query = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products, DIY tutorials...',
            'aria-label': 'Search'
        })
    )