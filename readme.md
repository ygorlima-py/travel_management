# Travel Management - Expense Tracking System

A Django-based web application for managing and tracking travel expenses with PostgreSQL database and Docker containerization.

## Project Overview

This application allows users to register, view, and manage travel expenses with detailed information including supplier details, location, amounts, and invoice images.

## Technology Stack

- **Backend Framework**: Django 5.2.8
- **Database**: PostgreSQL 17 (Alpine)
- **Container Orchestration**: Docker & Docker Compose
- **Image Processing**: Pillow 12.0.0
- **Database Driver**: psycopg2-binary 2.9.10
- **Environment Management**: python-dotenv 1.2.1

## Features

### Data Models

1. **Category Model**
   - Categorizes different types of expenses
   - Simple name field for classification

2. **State Model**
   - Brazilian state information
   - Includes full name and UF (state abbreviation)
   - Unique constraints on both fields

3. **Expenses Model**
   - Comprehensive expense tracking with the following fields:
     - Category (required, protected foreign key)
     - Supply/Supplier name
     - Location (State and City)
     - Invoice number (unique, 9 characters)
     - Date and time
     - Amount/Quantity
     - Total value (decimal with 2 places)
     - Detailed description
     - Invoice picture upload
     - Owner tracking (linked to User model)

### Views and Pages

1. **Index Page**
   - Displays all expenses in a paginated table (25 per page)
   - Shows: ID, Category, Supplier, City, State, Invoice Number, Date, Quantity, Total Value
   - Responsive table design with modern styling
   - Custom table caption with bordered title

2. **Expense Detail Page**
   - Modern card-based layout with responsive grid design
   - Organized into distinct information sections:
     - Basic Information Card (ID, Category, Supplier, Invoice Number)
     - Location Card (City, State, Date)
     - Values Card (Quantity, Total Value with highlighting)
     - Description Card (detailed expense description)
     - Invoice Image Card (with image preview and zoom effect)
   - Hover effects and smooth transitions
   - Professional styling with color-coded elements
   - Fallback messages for missing data

### Media Storage

- **Upload Directory**: `data/web/media/pictures/%Y/%m/`
- Images organized by year and month
- MEDIA_ROOT configured to: `BASE_DIR.parent / 'data' / 'web' / 'media'`
- Development server configured to serve media files when DEBUG is enabled

### UI/UX Enhancements

- Consistent color scheme using CSS custom properties
- Responsive design with mobile-first approach
- Card-based layouts with shadow effects
- Hover animations and transitions
- Professional typography and spacing
- Badge system for categories
- Highlighted value displays
- Image zoom effects on hover

## Project Structure

```
travel_management/
├── djangoapp/
│   ├── manage.py
│   ├── requirements.txt
│   ├── expenses/
│   │   ├── models.py          # Data models
│   │   ├── views.py           # View logic
│   │   ├── admin.py           # Admin configuration
│   │   ├── migrations/        # Database migrations
│   │   ├── static/
│   │   │   └── expenses/
│   │   │       └── css/
│   │   │           ├── style.css    # Custom styles
│   │   │           └── remedy.css   # CSS reset
│   │   └── templates/
│   │       └── expenses/
│   │           ├── base.html
│   │           ├── partials/
│   │           │   ├── _head.html
│   │           │   └── _header.html
│   │           └── pages/
│   │               ├── index.html    # Expense list
│   │               └── expense.html  # Expense detail
│   └── project/
│       ├── settings.py        # Django settings
│       ├── urls.py           # URL routing
│       ├── wsgi.py
│       └── asgi.py
├── data/
│   ├── postgres/data/        # PostgreSQL data volume
│   └── web/
│       └── media/
│           └── pictures/     # Uploaded invoice images
├── scripts/
│   ├── runserver.sh
│   ├── migrate.sh
│   ├── makemigrations.sh
│   ├── collectstatic.sh
│   └── wait_psql.sh
├── dotenv_files/
│   └── .env                  # Environment variables
├── docker-compose.yml
├── Dockerfile
└── readme.md
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed
- WSL (if running on Windows)

### Configuration

1. Create environment file in `dotenv_files/.env` with:
   - Database credentials
   - ALLOWED_HOSTS
   - SECRET_KEY
   - DEBUG settings

2. Build and run containers:
   ```bash
   docker-compose up --build
   ```

3. Run migrations:
   ```bash
   ./scripts/migrate.sh
   ```

4. Create superuser (optional):
   ```bash
   docker exec -it djangoapp python manage.py createsuperuser
   ```

### URL Routes

- `/` - Expense list (index page)
- `/despesa/<id>/detail` - Individual expense detail
- `/admin/` - Django admin panel

## Database Schema

- **Categories**: Expense classification system
- **States**: Brazilian states with UF codes
- **Expenses**: Main expense records with comprehensive fields
- **Users**: Built-in Django authentication (for expense ownership)

## Media Handling

Images are stored in a date-based directory structure:
- Format: `MEDIA_ROOT/pictures/YYYY/MM/filename.ext`
- Supports common image formats (JPEG, PNG)
- Served through Django development server when DEBUG=True

## Docker Configuration

Two services running in Docker:
1. **djangoapp**: Django application server on port 8000
2. **psql**: PostgreSQL database on port 5432

Volumes:
- PostgreSQL data persistence
- Static files volume
- Media files volume
- Bind mount for development code

## Development Notes

- Uses Django 5.2.8 with PostgreSQL backend
- Implements proper foreign key relationships with PROTECT and SET_NULL options
- Responsive design using CSS Grid and Flexbox
- Custom CSS properties for consistent theming
- Pagination implemented for expense list
- Image upload with automatic directory organization by date

## Future Enhancements

Potential improvements:
- User authentication and authorization
- Expense filtering and search functionality
- Export to CSV/PDF
- Expense analytics and reporting
- Multi-currency support
- Expense approval workflow
