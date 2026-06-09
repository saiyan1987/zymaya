# Zymaya Django Ecommerce Starter

A simple Django ecommerce project for **Zymaya**, styled with a clean luxury fashion theme inspired by boutique ecommerce layouts.

## Features

- Minimal luxury homepage
- Category browsing
- Product grid
- Product detail pages
- Multiple sizes/variants per product
- Stock per variant
- Session cart
- Demo checkout/order creation
- Django admin management
- Sample products fixture

## Run locally

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sample_data
python manage.py createsuperuser
python manage.py runserver
```

Open: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Notes

This is a starter/demo ecommerce site. Payments are not wired in yet. Stripe can be added later.
