# Credit Card Payment System

Full-stack project implementing modules from PDF requirements.

## Stack
- Backend: Django + Django REST Framework + JWT
- Payment microservice: FastAPI
- Frontend: React + Tailwind (skeleton)
- Database: MySQL
- Docker: docker-compose for all services

## Quick start
1. Install dependencies: `pip install -r requirements.txt`
2. Build and start all services: `docker-compose up --build`
3. Django API: http://localhost:8000/api/
4. FastAPI docs: http://localhost:8100/docs
5. Frontend: http://localhost:3000

## Modules covered
- Auth (register/login/logout, password hashing, protected routes)
- Card management (add/view/delete masked cards)
- Payment processing (PENDING → SUCCESS/FAILED)
- Transaction history filtering
- Admin panel (Django admin plus endpoints)
- Security rules (no CVV storage, input validation, JWT, SQL safety)
- API docs and docker

## Admin credentials
- username: admin
- password: Admin@123

## Notes
- For MySQL, update `.env` or container variables.
- Prepare DB and run migrations:
  - `docker-compose exec django python manage.py migrate`
  - `docker-compose exec django python manage.py createsuperuser`
