from django.conf import settings

def media_url(request):
    """Add media URL to the context of all templates"""
    return {'MEDIA_URL': settings.MEDIA_URL}