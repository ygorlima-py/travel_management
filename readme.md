# Django Project Template with Docker

A ready-to-use Django project boilerplate with Docker and PostgreSQL configuration. This template provides a solid foundation for quickly bootstrapping Django applications with containerization support.

## 🚀 Features

- **Django 5.2.8** - Latest Django framework
- **Docker & Docker Compose** - Containerized development environment
- **PostgreSQL 17** - Production-ready database (Alpine-based)
- **Python 3.11.14** - Alpine-based lightweight image
- **Environment Variables** - Configuration via `.env` files
- **Static & Media Files** - Pre-configured volume management
- **Helper Scripts** - Automated commands for common Django tasks

## 📋 Prerequisites

- Docker
- Docker Compose
- Git (optional)

## 🛠️ Project Structure

```
.
├── djangoapp/             # Django application directory
│   ├── app-example/       # Sample app (app-example)
│   └── project/           # Django project settings
├── scripts/               # Helper shell scripts
│   ├── commands.sh        # Main command executor
│   ├── wait_psql.sh       # PostgreSQL health check
│   ├── collectstatic.sh   # Collect static files
│   ├── makemigrations.sh  # Generate migrations
│   ├── migrate.sh         # Apply migrations
│   └── runserver.sh       # Start development server
├── dotenv_files/          # Environment configuration files
├── data/                  # Persistent data (auto-created)
│   ├── postgres/data/     # PostgreSQL data
│   └── web/              
│       ├── static/        # Static files
│       └── media/         # Media uploads
├── docker-compose.yml     # Docker services configuration
├── Dockerfile            # Django app container definition
└── requirements.txt      # Python dependencies
```

## 🔧 Setup & Usage

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd django_docker_template
```

### Step 2: Configure Environment Variables

Create a `.env` file inside the `dotenv_files/` directory:

```bash
# dotenv_files/.env

# PostgreSQL Configuration
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_secure_password

# Django Configuration (optional)
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**💡 Tip:** If the `.env` file doesn't exist, create it manually:

```bash
mkdir -p dotenv_files
touch dotenv_files/.env
```

### Step 3: Build and Start the Containers

```bash
docker-compose up --build
```

**What happens in this command:**
- 🔨 Builds the Django Docker image
- 📦 Downloads the PostgreSQL 17 image
- 🚀 Starts the `djangoapp` and `psql` containers
- ✅ Waits for PostgreSQL to be ready
- 📂 Collects static files (`collectstatic`)
- 🗄️ Runs database migrations
- 🌐 Starts the development server

**Wait for the message:**
```
Starting development server at http://0.0.0.0:8000/
```

The application will be available at: **http://localhost:8000**

### Step 4: Create a Superuser (Optional)

To access Django Admin, create a superuser:

```bash
docker-compose exec djangoapp python manage.py createsuperuser
```

Access the admin at: **http://localhost:8000/admin**

### Step 5: Stop the Containers

To stop the containers without removing data:

```bash
docker-compose down
```

To stop AND remove volumes (⚠️ deletes data):

```bash
docker-compose down -v
```

## 📦 Included Dependencies

- **Django 5.2.8** - Web framework
- **python-dotenv 1.2.1** - Environment variable management
- **psycopg2-binary 2.9.10** - PostgreSQL database driver

## 🔐 Security Notes

⚠️ **Important**: This template includes a default `SECRET_KEY` in `settings.py`. 

**Before deploying to production:**
- Generate a new secret key
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` properly
- Use environment variables for sensitive data
- Review and update all security settings

## 🐳 Docker Configuration

### Services

**djangoapp**
- Container: Django application
- Port: 8000
- Volumes: Code, static files, media files
- Depends on: PostgreSQL

**psql**
- Container: PostgreSQL database
- Image: postgres:17-alpine
- Persistent storage for database data

### Custom User

The Dockerfile creates a non-root user (`duser`) for running the application, following security best practices.

## 📝 Helper Scripts

All scripts are located in the `scripts/` directory and are automatically executable:

- `commands.sh` - Orchestrates all initialization commands
- `wait_psql.sh` - Waits for PostgreSQL to be ready
- `collectstatic.sh` - Collects Django static files
- `makemigrations.sh` - Creates database migrations
- `migrate.sh` - Applies database migrations
- `runserver.sh` - Starts the Django development server

## 🎯 Next Steps

After setting up the template, you can:

1. **Create new Django apps:**
   ```bash
   docker-compose exec djangoapp python manage.py startapp myapp
   ```

2. **Add your app to `INSTALLED_APPS`** in `djangoapp/project/settings.py`

3. **Create models** in your app's `models.py`

4. **Run migrations:**
   ```bash
   docker-compose exec djangoapp python manage.py makemigrations
   docker-compose exec djangoapp python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   docker-compose exec djangoapp python manage.py createsuperuser
   ```

## 🔄 Common Commands

```bash
# Access Django shell
docker-compose exec djangoapp python manage.py shell

# Run tests
docker-compose exec djangoapp python manage.py test

# View logs
docker-compose logs -f djangoapp

# Rebuild containers
docker-compose up --build -d

# Access container bash
docker-compose exec djangoapp sh
```

## 📄 License

This is a code snippet template for reuse in Django projects. Feel free to modify and adapt to your needs.

## 👤 Maintainer

**Email:** ygor.limarsx@gmail.com

---

**Note:** This is a boilerplate/template project designed to be reused and customized for building Django applications quickly. Modify according to your specific requirements.
