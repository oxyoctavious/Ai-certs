# Django Intern Assignment

Modular Django REST Framework backend for managing vendors, products, courses, certifications, and their mappings using `APIView` only.

## Tech Stack

- Django
- Django REST Framework
- drf-yasg
- SQLite

## Installed Apps

- `common`
- `vendor`
- `product`
- `course`
- `certification`
- `vendor_product_mapping`
- `product_course_mapping`
- `course_certification_mapping`

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Seed sample data:

```bash
python manage.py seed_data
```

4. Start the server:

```bash
python manage.py runserver
```

## API Documentation

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## API Usage Examples

```bash
curl http://127.0.0.1:8000/api/vendors/
curl http://127.0.0.1:8000/api/products/?vendor_id=1
curl http://127.0.0.1:8000/api/courses/?product_id=1
curl http://127.0.0.1:8000/api/certifications/?course_id=1
```

```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d "{\"vendor\": 1, \"product\": 1, \"primary_mapping\": true}"
```

## Notes

- Every required app contains its own `models.py`, `serializers.py`, `views.py`, `urls.py`, and `admin.py`.
- CRUD endpoints are implemented with `APIView` only.
- Delete endpoints perform soft delete by setting `is_active=False`.
- Mapping validations prevent duplicate active pairs and multiple primary mappings for the same parent.
