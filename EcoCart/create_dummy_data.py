import os
import django
import random
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecocart.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from greenapp.models import (
    Category, Product, Review, DIY, DIYComment, 
    WishlistItem, VisitLog, ExternalResource, ContactMessage, Newsletter
)

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print("Superuser created.")

# Create regular users
users = []
for i in range(1, 6):
    username = f"user{i}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=f"user{i}@example.com",
            password="password123",
            first_name=f"User{i}",
            last_name=f"Test"
        )
        users.append(user)
        print(f"Created user: {username}")
    else:
        users.append(User.objects.get(username=username))

if not users:
    users = list(User.objects.all())

# Create categories
categories = [
    {"name": "Kitchen", "description": "Eco-friendly kitchen products"},
    {"name": "Bathroom", "description": "Sustainable bathroom essentials"},
    {"name": "Cleaning", "description": "Green cleaning solutions"},
    {"name": "Garden", "description": "Eco-friendly gardening products"},
    {"name": "Energy", "description": "Energy-efficient products"},
]

created_categories = []
for category_data in categories:
    slug = slugify(category_data["name"])
    category, created = Category.objects.get_or_create(
        slug=slug,
        defaults={
            "name": category_data["name"],
            "description": category_data["description"]
        }
    )
    created_categories.append(category)
    if created:
        print(f"Created category: {category.name}")

# Create products
products = [
    {
        "name": "Bamboo Cutlery Set",
        "category": "Kitchen",
        "description": "Reusable bamboo cutlery set with carrying case",
        "price": 12.99,
        "is_reusable": True,
        "is_biodegradable": True
    },
    {
        "name": "Stainless Steel Water Bottle",
        "category": "Kitchen",
        "description": "Durable stainless steel water bottle, BPA-free",
        "price": 24.99,
        "is_reusable": True,
        "is_recyclable": True
    },
    {
        "name": "Beeswax Food Wraps",
        "category": "Kitchen",
        "description": "Reusable food wraps made from organic cotton and beeswax",
        "price": 18.50,
        "is_reusable": True,
        "is_biodegradable": True,
        "is_organic": True
    },
    {
        "name": "Bamboo Toothbrush",
        "category": "Bathroom",
        "description": "Biodegradable toothbrush with bamboo handle",
        "price": 4.99,
        "is_biodegradable": True,
        "is_compostable": True
    },
    {
        "name": "Organic Cotton Towels",
        "category": "Bathroom",
        "description": "Soft towels made from 100% organic cotton",
        "price": 29.99,
        "is_organic": True,
        "is_biodegradable": True
    },
    {
        "name": "Natural Loofah Sponge",
        "category": "Bathroom",
        "description": "Natural loofah sponge for exfoliation",
        "price": 6.99,
        "is_biodegradable": True,
        "is_compostable": True,
        "is_organic": True
    },
    {
        "name": "All-Purpose Cleaner Concentrate",
        "category": "Cleaning",
        "description": "Plant-based cleaning concentrate in a glass bottle",
        "price": 15.99,
        "is_biodegradable": True,
        "is_organic": True
    },
    {
        "name": "Wool Dryer Balls",
        "category": "Cleaning",
        "description": "Reusable wool dryer balls to replace dryer sheets",
        "price": 19.99,
        "is_reusable": True,
        "is_organic": True
    },
    {
        "name": "Compostable Trash Bags",
        "category": "Cleaning",
        "description": "Trash bags that break down in compost",
        "price": 8.99,
        "is_compostable": True,
        "is_biodegradable": True
    },
    {
        "name": "Compost Bin",
        "category": "Garden",
        "description": "Outdoor compost bin for garden waste",
        "price": 89.99,
        "is_reusable": True
    },
    {
        "name": "Rain Barrel",
        "category": "Garden",
        "description": "Collect rainwater for garden use",
        "price": 119.99,
        "is_reusable": True
    },
    {
        "name": "Organic Seeds Pack",
        "category": "Garden",
        "description": "Variety pack of organic vegetable seeds",
        "price": 14.99,
        "is_organic": True
    },
    {
        "name": "Solar Garden Lights",
        "category": "Energy",
        "description": "Path lights powered by solar energy",
        "price": 34.99,
        "is_energy_efficient": True,
        "is_reusable": True
    },
    {
        "name": "LED Light Bulbs (4-pack)",
        "category": "Energy",
        "description": "Energy-efficient LED bulbs",
        "price": 12.99,
        "is_energy_efficient": True,
        "is_recyclable": True
    },
    {
        "name": "Solar Phone Charger",
        "category": "Energy",
        "description": "Portable phone charger with solar panel",
        "price": 49.99,
        "is_energy_efficient": True,
        "is_reusable": True
    }
]

created_products = []
for product_data in products:
    category_name = product_data.pop("category")
    category = next((c for c in created_categories if c.name == category_name), None)
    
    if category:
        slug = slugify(product_data["name"])
        product, created = Product.objects.get_or_create(
            slug=slug,
            defaults={
                **product_data,
                "category": category
            }
        )
        created_products.append(product)
        if created:
            print(f"Created product: {product.name}")

# Create reviews
if created_products:
    for product in created_products:
        # Create 2-5 reviews per product
        for _ in range(random.randint(2, 5)):
            user = random.choice(users)
            # Skip if user already reviewed this product
            if not Review.objects.filter(user=user, product=product).exists():
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    comment=f"This is a review for {product.name}. It's a great eco-friendly product!"
                )
                print(f"Created review for {product.name} by {user.username}")

# Create DIY tutorials
diy_tutorials = [
    {
        "title": "Homemade All-Purpose Cleaner",
        "category": "Cleaning",
        "description": "Make your own all-purpose cleaner with simple ingredients",
        "materials": "- 1 cup white vinegar\n- 1 cup water\n- 10 drops essential oil (optional)\n- Spray bottle",
        "instructions": "1. Mix vinegar and water in a spray bottle\n2. Add essential oils if desired\n3. Shake well before use\n4. Use on most surfaces except marble and granite",
        "difficulty": "easy",
        "time_required": "5 minutes"
    },
    {
        "title": "DIY Beeswax Wraps",
        "category": "Kitchen",
        "description": "Make your own reusable food wraps as an alternative to plastic wrap",
        "materials": "- Cotton fabric\n- Beeswax pellets\n- Jojoba oil\n- Pine resin (optional)\n- Parchment paper\n- Iron\n- Scissors",
        "instructions": "1. Cut fabric to desired sizes\n2. Place fabric on parchment paper\n3. Sprinkle beeswax pellets over fabric\n4. Add a few drops of jojoba oil\n5. Cover with another sheet of parchment paper\n6. Iron on low heat until wax melts\n7. Let cool and trim edges if needed",
        "difficulty": "medium",
        "time_required": "30 minutes"
    },
    {
        "title": "Mason Jar Herb Garden",
        "category": "Garden",
        "description": "Create a small indoor herb garden using mason jars",
        "materials": "- Mason jars\n- Small rocks or pebbles\n- Potting soil\n- Herb seeds or small plants\n- Labels\n- Twine or ribbon (optional)",
        "instructions": "1. Place a layer of small rocks at the bottom of each jar for drainage\n2. Add potting soil, leaving about an inch at the top\n3. Plant seeds or small herb plants\n4. Water lightly\n5. Place in a sunny spot\n6. Label each jar\n7. Water when soil feels dry",
        "difficulty": "easy",
        "time_required": "20 minutes"
    },
    {
        "title": "Upcycled T-shirt Tote Bag",
        "category": "Cleaning",
        "description": "Turn an old t-shirt into a reusable shopping bag",
        "materials": "- Old t-shirt\n- Scissors\n- Ruler\n- Pen or chalk",
        "instructions": "1. Cut off the sleeves of the t-shirt\n2. Cut a wider neck opening\n3. Turn the shirt inside out\n4. Draw a line about 2 inches from the bottom\n5. Cut fringe strips up to the line\n6. Tie each pair of fringe strips together\n7. Turn right side out and your bag is ready",
        "difficulty": "easy",
        "time_required": "15 minutes"
    },
    {
        "title": "DIY Solar Water Heater",
        "category": "Energy",
        "description": "Build a simple solar water heater for your garden or camping",
        "materials": "- Garden hose (black preferred)\n- Plywood board\n- Aluminum foil\n- Clear plastic sheet\n- Staple gun\n- Hose connectors",
        "instructions": "1. Cover the plywood with aluminum foil, shiny side up\n2. Coil the hose on the foil-covered board\n3. Secure the hose with staples\n4. Cover with clear plastic to create a greenhouse effect\n5. Connect to water source\n6. Place in direct sunlight\n7. Allow water to heat up before use",
        "difficulty": "hard",
        "time_required": "2 hours"
    }
]

created_diy_tutorials = []
for diy_data in diy_tutorials:
    category_name = diy_data.pop("category")
    category = next((c for c in created_categories if c.name == category_name), None)
    
    if category:
        slug = slugify(diy_data["title"])
        author = random.choice(users)
        diy, created = DIY.objects.get_or_create(
            slug=slug,
            defaults={
                **diy_data,
                "category": category,
                "author": author
            }
        )
        created_diy_tutorials.append(diy)
        if created:
            print(f"Created DIY tutorial: {diy.title}")

# Create DIY comments
if created_diy_tutorials:
    for diy in created_diy_tutorials:
        # Create 1-3 comments per DIY tutorial
        for _ in range(random.randint(1, 3)):
            user = random.choice(users)
            DIYComment.objects.create(
                diy=diy,
                user=user,
                comment=f"I tried this {diy.title} tutorial and it worked great! Thanks for sharing."
            )
            print(f"Created comment for {diy.title} by {user.username}")

# Create wishlist items
if created_products and users:
    for user in users:
        # Add 2-4 random products to each user's wishlist
        for product in random.sample(created_products, random.randint(2, 4)):
            if not WishlistItem.objects.filter(user=user, product=product).exists():
                WishlistItem.objects.create(
                    user=user,
                    product=product
                )
                print(f"Added {product.name} to {user.username}'s wishlist")

# Create visit logs
if users:
    pages = [
        "Home Page",
        "Product: Bamboo Cutlery Set",
        "Product: Stainless Steel Water Bottle",
        "DIY: Homemade All-Purpose Cleaner",
        "DIY: Mason Jar Herb Garden",
        "Category: Kitchen",
        "Category: Bathroom",
        "Search Results"
    ]
    
    for user in users:
        # Create 5-10 visit logs per user
        for _ in range(random.randint(5, 10)):
            page = random.choice(pages)
            time_spent = timedelta(minutes=random.randint(1, 15))
            VisitLog.objects.create(
                user=user,
                page_visited=page,
                ip_address="127.0.0.1",
                time_spent=time_spent
            )
        print(f"Created visit logs for {user.username}")

# Create external resources
resources = [
    {
        "title": "Environment and Climate Change Canada",
        "url": "https://www.canada.ca/en/environment-climate-change.html",
        "description": "Official website of Environment and Climate Change Canada with resources on environmental protection.",
        "category": "Cleaning"
    },
    {
        "title": "ENERGY STAR Canada",
        "url": "https://www.nrcan.gc.ca/energy-efficiency/energy-star-canada/18953",
        "description": "ENERGY STAR Canada is the mark of high-efficiency products in Canada.",
        "category": "Energy"
    },
    {
        "title": "Canadian Gardening",
        "url": "https://gardenmaking.com/",
        "description": "Resource for organic and sustainable gardening practices in Canada.",
        "category": "Garden"
    },
    {
        "title": "Zero Waste Canada",
        "url": "https://zerowastecanada.ca/",
        "description": "Canadian non-profit organization dedicated to promoting zero waste principles.",
        "category": "Kitchen"
    },
    {
        "title": "David Suzuki Foundation",
        "url": "https://davidsuzuki.org/",
        "description": "Canadian non-profit organization promoting environmental sustainability and conservation.",
        "category": "Bathroom"
    }
]

for resource_data in resources:
    category_name = resource_data.pop("category")
    category = next((c for c in created_categories if c.name == category_name), None)
    
    if category:
        resource, created = ExternalResource.objects.get_or_create(
            url=resource_data["url"],
            defaults={
                **resource_data,
                "category": category
            }
        )
        if created:
            print(f"Created external resource: {resource.title}")

# Create newsletter subscriptions
emails = [
    "subscriber1@example.com",
    "subscriber2@example.com",
    "subscriber3@example.com",
    "subscriber4@example.com",
    "subscriber5@example.com"
]

for email in emails:
    if not Newsletter.objects.filter(email=email).exists():
        Newsletter.objects.create(email=email)
        print(f"Created newsletter subscription for {email}")

# Create contact messages
messages = [
    {
        "name": "John Smith",
        "email": "john@example.com",
        "subject": "Question about bamboo products",
        "message": "I'm interested in your bamboo products. Are they sourced sustainably?"
    },
    {
        "name": "Sarah Johnson",
        "email": "sarah@example.com",
        "subject": "Bulk ordering",
        "message": "Do you offer discounts for bulk orders of your eco-friendly products?"
    },
    {
        "name": "Michael Brown",
        "email": "michael@example.com",
        "subject": "Shipping within Canada",
        "message": "Do you offer free shipping within Canada for orders over $50?"
    }
]

for message_data in messages:
    ContactMessage.objects.create(**message_data)
    print(f"Created contact message from {message_data['name']}")

print("\nDummy data creation complete!")