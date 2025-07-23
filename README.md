# TLP-Taller-Python

Juan Estiven Carmona Muñoz - CC 1000567015

# Punto 1 - API de Gestión de Biblioteca

Esta es una API para la gestión de una biblioteca desarrollada con **FastAPI** que incluye funcionalidades para manejar autores, libros y préstamos.

## Características

### Entidades Principales
- **Autores**: Gestión de información de autores
- **Libros**: Catálogo de libros con información detallada
- **Préstamos**: Sistema de préstamos y devoluciones

### Funcionalidades Implementadas

#### 1. **Listado de Entidades**
- `GET /authors/` - Lista todos los autores
- `GET /books/` - Lista todos los libros
- `GET /loans/` - Lista todos los préstamos

#### 2. **Creación de Entidades**
- `POST /authors/` - Crear nuevo autor
- `POST /books/` - Crear nuevo libro
- `POST /loans/` - Crear nuevo préstamo

#### 3. **Eliminación de Entidades**
- `DELETE /authors/{id}` - Eliminar autor
- `DELETE /books/{id}` - Eliminar libro
- `DELETE /loans/{id}` - Eliminar préstamo

#### 4. **Transformaciones**
- `PATCH /books/{id}/discount` - Aplicar descuento a libro
- `PATCH /loans/{id}/return` - Devolver libro prestado
- `PUT /books/{id}` - Modificar información del libro
- `PUT /authors/{id}` - Modificar información del autor

### Funcionalidades Adicionales
- `GET /books/available` - Libros disponibles para préstamo
- `GET /loans/active` - Préstamos activos (no devueltos)
- `GET /loans/user/{email}` - Préstamos por usuario

## Requisitos del Sistema

### Casos de Uso Principales

1. **Gestión de Autores**
   - Registrar nuevos autores con información básica
   - Consultar lista de autores
   - Actualizar información de autores
   - Eliminar autores (solo si no tienen libros asociados)

2. **Gestión de Libros**
   - Agregar libros al catálogo
   - Consultar disponibilidad de libros
   - Aplicar descuentos a precios
   - Modificar información (páginas, precio, etc.)
   - Eliminar libros (solo si no tienen préstamos activos)

3. **Gestión de Préstamos**
   - Crear préstamos de libros disponibles
   - Registrar devoluciones
   - Consultar historial de préstamos
   - Consultar préstamos por usuario

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd library_api
```

2. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up --build
```

3. **Acceder a la API**
- API: http://localhost:8001
- Documentación Swagger: http://localhost:8001/docs
- Documentación ReDoc: http://localhost:8001/redoc

### Opción 2: Instalación Local

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload
```

## Ejecutar Pruebas

### Con Docker
```bash
docker-compose exec library-api pytest tests/ -v
```

### Local
```bash
pytest tests/ -v
```

## Base de Datos

La aplicación utiliza **SQLite** como base de datos en memoria para desarrollo y pruebas. La base de datos se crea automáticamente al iniciar la aplicación con todas las tablas y relaciones necesarias.

### Relaciones
- Un **Autor** puede tener múltiples **Libros**
- Un **Libro** puede tener múltiples **Préstamos**
- Un **Préstamo** pertenece a un **Libro** específico

## API Endpoints

### Autores
- `GET /authors/` - Listar autores
- `POST /authors/` - Crear autor
- `GET /authors/{id}` - Obtener autor por ID
- `PUT /authors/{id}` - Actualizar autor
- `DELETE /authors/{id}` - Eliminar autor

### Libros
- `GET /books/` - Listar libros
- `POST /books/` - Crear libro
- `GET /books/{id}` - Obtener libro por ID
- `PUT /books/{id}` - Actualizar libro
- `DELETE /books/{id}` - Eliminar libro
- `GET /books/available` - Libros disponibles
- `PATCH /books/{id}/discount` - Aplicar descuento

### Préstamos
- `GET /loans/` - Listar préstamos
- `POST /loans/` - Crear préstamo
- `GET /loans/{id}` - Obtener préstamo por ID
- `DELETE /loans/{id}` - Eliminar préstamo
- `GET /loans/active` - Préstamos activos
- `GET /loans/user/{email}` - Préstamos por usuario
- `PATCH /loans/{id}/return` - Devolver libro

## Ejemplos de Uso

### 1. Crear un Autor
```bash
curl -X POST "http://localhost:8001/authors/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Gabriel García Márquez",
       "nationality": "Colombian",
       "birth_year": 1927
     }'
```

### 2. Crear un Libro
```bash
curl -X POST "http://localhost:8001/books/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Cien años de soledad",
       "isbn": "978-0307474728",
       "pages": 417,
       "price": 25.99,
       "author_id": 1
     }'
```

### 3. Crear un Préstamo
```bash
curl -X POST "http://localhost:8001/loans/" \
     -H "Content-Type: application/json" \
     -d '{
       "user_name": "Juan Pérez",
       "user_email": "juan.perez@email.com",
       "book_id": 1
     }'
```

### 4. Aplicar Descuento a un Libro
```bash
curl -X PATCH "http://localhost:8001/books/1/discount" \
     -H "Content-Type: application/json" \
     -d '{
       "discount_percentage": 20.0
     }'
```

### 5. Devolver un Libro
```bash
curl -X PATCH "http://localhost:8001/loans/1/return"
```

## Validaciones Implementadas

### Libros
- ISBN único por libro
- Verificación de existencia del autor
- No se pueden eliminar libros con préstamos activos
- Descuentos válidos (0-100%)

### Autores
- No se pueden eliminar autores con libros asociados

### Préstamos
- Solo se pueden prestar libros disponibles
- Un libro prestado no está disponible para otros préstamos
- Al devolver un libro, queda disponible nuevamente

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **Pydantic**: Validación de datos y serialización
- **SQLite**: Base de datos ligera
- **Pytest**: Framework de testing
- **Docker**: Containerización
- **Uvicorn**: Servidor ASGI

## Documentación API

La API incluye documentación automática generada por FastAPI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

# Punto 2 - IMDB Horror Movies

## Instalación y Ejecución

### Opción 1: Con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd horror-movies-IMDB
```

2. **Construir y ejecutar con Docker**
```bash
docker build -t horror-movie-analysis .
docker run --rm horror-movie-analysis
```

### Opción 2: Instalación Local

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## Ejecutar Pruebas

### Con Docker
```bash
docker run --rm horror-movie-analysis python test.py
```

### Local
```bash
python test.py
```

# Licencia

Este proyecto está bajo la Licencia MIT.
