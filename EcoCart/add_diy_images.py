import os
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecocart.settings')
django.setup()

from greenapp.models import DIY

# Create media directory if it doesn't exist
os.makedirs('media/diy/2025/07/16', exist_ok=True)

# Sample image URLs for DIY tutorials
diy_images = {
    'homemade-all-purpose-cleaner': 'https://images.pexels.com/photos/4239013/pexels-photo-4239013.jpeg?auto=compress&cs=tinysrgb&w=600',
    'diy-beeswax-wraps': 'https://images.pexels.com/photos/6152391/pexels-photo-6152391.jpeg?auto=compress&cs=tinysrgb&w=600',
    'mason-jar-herb-garden': 'https://images.pexels.com/photos/1407305/pexels-photo-1407305.jpeg?auto=compress&cs=tinysrgb&w=600',
    'upcycled-t-shirt-tote-bag': 'https://images.pexels.com/photos/5650026/pexels-photo-5650026.jpeg?auto=compress&cs=tinysrgb&w=600',
    'diy-solar-water-heater': 'https://images.pexels.com/photos/9875441/pexels-photo-9875441.jpeg?auto=compress&cs=tinysrgb&w=600',
}

# Download and save images for DIY tutorials
for slug, image_url in diy_images.items():
    try:
        diy = DIY.objects.get(slug=slug)
        
        # Skip if DIY already has an image
        if diy.image:
            print(f"DIY tutorial '{diy.title}' already has an image. Skipping.")
            continue
        
        # Download image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save image to DIY tutorial
            image_name = f"{slug}.jpg"
            diy.image.save(image_name, ContentFile(response.content), save=True)
            print(f"Added image to DIY tutorial: {diy.title}")
        else:
            print(f"Failed to download image for {diy.title}. Status code: {response.status_code}")
    
    except DIY.DoesNotExist:
        print(f"DIY tutorial with slug '{slug}' not found.")
    except Exception as e:
        print(f"Error adding image to {slug}: {str(e)}")

print("DIY tutorial image update complete!")