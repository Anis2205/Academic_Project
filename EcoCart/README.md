# EcoCart - A Green Shopping Assistant

A Django-based web platform designed to promote sustainable and eco-friendly shopping habits by offering a curated catalog of environmentally friendly products, user-submitted DIY green alternatives, and community-driven reviews.

## Project Overview

EcoCart is a comprehensive web application that helps users discover eco-friendly products, share reviews, and learn how to create sustainable alternatives through DIY tutorials. The platform encourages sustainable consumer choices through a collaborative environment focused on green living.

## Key Features

1. **Browse Eco-Friendly Products**
   - View a curated list of environmentally friendly products with detailed info and sustainability tags
   - Filter products by category, price range, and eco-friendly attributes

2. **Product Details & Reviews**
   - View product information, ratings, and user reviews
   - Authenticated users can submit their own reviews

3. **Search & Filter**
   - Search products and DIY tutorials with filters (category, rating, tags)
   - Global search across the entire platform

4. **User Registration & Login**
   - Create accounts, log in securely, manage profile
   - Password reset functionality

5. **Submit Product Reviews**
   - Authenticated users can rate and review products
   - Earn eco-points for contributing reviews

6. **Upload DIY Tutorials**
   - Registered users can upload eco-friendly DIY tutorials with images and descriptions
   - Share materials, instructions, and difficulty level

7. **Wishlist Management**
   - Users save favorite products for quick access
   - Easy add/remove functionality

8. **Visit History Tracking**
   - Track and display user's browsing history and interactions
   - Provide personalized insights based on activity

9. **External Resources**
   - Curated links to trusted green websites for educational purposes
   - Categorized by sustainability topics

10. **Contact & About Pages**
    - Information about the project and contact form for inquiries
    - Newsletter subscription

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd EcoCart
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the site at http://127.0.0.1:8000/

## Project Structure

- `ecocart/` - Main project directory
  - `ecocart/` - Project settings and configuration
  - `greenapp/` - Main application with models, views, and forms
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
  - `media/` - User-uploaded files

## Technologies Used

- Django 4.2
- Bootstrap 5
- SQLite (development)
- HTML5, CSS3, JavaScript
- Font Awesome icons

## User Roles and Access

- **Guest (Unauthenticated)**: Browse products, view product & DIY details, search, view static pages, external resources.
- **Registered User**: All guest permissions + submit reviews, upload DIYs, manage wishlist, view dashboard and visit history.

## Created for COMP-8347 Course Project