import os
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecocart.settings')
django.setup()

from greenapp.models import Product

# Create media directory if it doesn't exist
os.makedirs('media/products/2025/07/16', exist_ok=True)

# Sample image URLs for products
product_images = {
    'bamboo-cutlery-set': 'https://images.pexels.com/photos/4226896/pexels-photo-4226896.jpeg?auto=compress&cs=tinysrgb&w=600',
    'stainless-steel-water-bottle': 'https://images.pexels.com/photos/4000090/pexels-photo-4000090.jpeg?auto=compress&cs=tinysrgb&w=600',
    'beeswax-food-wraps': 'https://images.pexels.com/photos/6152391/pexels-photo-6152391.jpeg?auto=compress&cs=tinysrgb&w=600',
    'bamboo-toothbrush': 'https://images.pexels.com/photos/3737599/pexels-photo-3737599.jpeg?auto=compress&cs=tinysrgb&w=600',
    'organic-cotton-towels': 'https://images.pexels.com/photos/4210342/pexels-photo-4210342.jpeg?auto=compress&cs=tinysrgb&w=600',
    'natural-loofah-sponge': 'https://images.pexels.com/photos/7262393/pexels-photo-7262393.jpeg?auto=compress&cs=tinysrgb&w=600',
    'all-purpose-cleaner-concentrate': 'https://images.pexels.com/photos/4239013/pexels-photo-4239013.jpeg?auto=compress&cs=tinysrgb&w=600',
    'wool-dryer-balls': 'https://images.pexels.com/photos/6044266/pexels-photo-6044266.jpeg?auto=compress&cs=tinysrgb&w=600',
    'compostable-trash-bags': 'https://images.pexels.com/photos/5725742/pexels-photo-5725742.jpeg?auto=compress&cs=tinysrgb&w=600',
    'compost-bin': 'https://images.pexels.com/photos/6963622/pexels-photo-6963622.jpeg?auto=compress&cs=tinysrgb&w=600',
    'rain-barrel': 'https://images.pexels.com/photos/2749165/pexels-photo-2749165.jpeg?auto=compress&cs=tinysrgb&w=600',
    'organic-seeds-pack': 'https://images.pexels.com/photos/7728082/pexels-photo-7728082.jpeg?auto=compress&cs=tinysrgb&w=600',
    'solar-garden-lights': 'https://images.pexels.com/photos/1108701/pexels-photo-1108701.jpeg?auto=compress&cs=tinysrgb&w=600',
    'led-light-bulbs-4-pack': 'https://images.pexels.com/photos/3566358/pexels-photo-3566358.jpeg?auto=compress&cs=tinysrgb&w=600',
    'solar-phone-charger': 'https://images.pexels.com/photos/6667360/pexels-photo-6667360.jpeg?auto=compress&cs=tinysrgb&w=600',
}

# Download and save images for products
for slug, image_url in product_images.items():
    try:
        product = Product.objects.get(slug=slug)
        
        # Skip if product already has an image
        if product.image:
            print(f"Product '{product.name}' already has an image. Skipping.")
            continue
        
        # Download image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save image to product
            image_name = f"{slug}.jpg"
            product.image.save(image_name, ContentFile(response.content), save=True)
            print(f"Added image to product: {product.name}")
        else:
            print(f"Failed to download image for {product.name}. Status code: {response.status_code}")
    
    except Product.DoesNotExist:
        print(f"Product with slug '{slug}' not found.")
    except Exception as e:
        print(f"Error adding image to {slug}: {str(e)}")

print("Product image update complete!")