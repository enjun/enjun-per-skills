# Technology Stack Adaptation

Guidelines for analyzing different technology stacks when creating course materials.

## Analysis Process

For any source code repository, follow this analysis workflow:

1. **Identify build configuration files**
2. **Determine programming language**
3. **Identify frameworks and libraries**
4. **Understand project structure**
5. **Map core modules**

## Java Projects

### Spring Boot

**Build files to look for:**
- `pom.xml` (Maven)
- `build.gradle` or `build.gradle.kts` (Gradle)

**Key indicators:**
```xml
<!-- pom.xml -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

**Typical structure:**
```
src/main/java/com/example/
├── controller/      # REST controllers
├── service/         # Business logic
├── repository/      # Data access (JPA)
├── model/           # Entity classes
├── dto/             # Data transfer objects
└── config/          # Configuration classes
```

**Configuration files:**
- `application.properties` or `application.yml`
- `application-dev.properties`, `application-prod.properties`

### Jakarta Servlet (Traditional Java Web)

**Build files to look for:**
- `pom.xml` with servlet dependency

**Key indicators:**
```xml
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>6.0.0</version>
</dependency>
```

**Typical structure:**
```
src/main/java/com/example/
├── controller/      # Servlets (@WebServlet)
├── service/         # Business logic
├── dao/             # Data access
├── model/           # Entity classes
└── util/            # Utility classes
src/main/webapp/
├── WEB-INF/
│   └── web.xml      # Servlet configuration (optional)
├── jsp/             # JSP pages
└── static/          # CSS, JS, images
```

**Configuration files:**
- `web.xml` (traditional deployment descriptor)
- `context.xml` (database connection pool)

## Python Projects

### Django

**Files to look for:**
- `requirements.txt`
- `manage.py`
- `settings.py`

**Key indicators:**
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'myapp',
]
```

**Typical structure:**
```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── myapp/
    ├── models.py      # Database models
    ├── views.py       # Request handlers
    ├── urls.py        # URL routing
    ├── forms.py       # Form definitions
    └── templates/     # HTML templates
```

### Flask

**Files to look for:**
- `requirements.txt`
- `app.py` or `main.py`

**Key indicators:**
```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
```

**Typical structure:**
```
myproject/
├── app.py
├── requirements.txt
├── templates/        # HTML templates
├── static/           # CSS, JS, images
└── myapp/
    ├── models.py
    ├── views.py
    └── forms.py
```

### FastAPI

**Files to look for:**
- `requirements.txt` or `pyproject.toml`
- `main.py`

**Key indicators:**
```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## JavaScript/Node.js Projects

### Express

**Files to look for:**
- `package.json`

**Key indicators:**
```json
{
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

**Typical structure:**
```
myproject/
├── package.json
├── server.js or app.js
├── routes/           # Route definitions
├── controllers/      # Request handlers
├── services/         # Business logic
├── models/           # Database models
├── middleware/       # Express middleware
├── views/            # Template files
└── public/           # Static files
```

### NestJS

**Files to look for:**
- `package.json`
- `nest-cli.json`

**Key indicators:**
```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0"
  }
}
```

**Typical structure:**
```
myproject/
├── package.json
├── nest-cli.json
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── controllers/  # Controller classes
│   ├── services/     # Service classes
│   ├── models/       # DTOs and entities
│   └── modules/      # Feature modules
```

## PHP Projects

### Laravel

**Files to look for:**
- `composer.json`
- `artisan`

**Key indicators:**
```json
{
  "require": {
    "laravel/framework": "^10.0"
  }
}
```

**Typical structure:**
```
myproject/
├── composer.json
├── artisan
├── app/
│   ├── Http/
│   │   ├── Controllers/  # Controllers
│   │   ├── Middleware/   # Middleware
│   │   └── Requests/     # Form requests
│   ├── Models/           # Eloquent models
│   └── Services/         # Business logic
├── resources/
│   ├── views/           # Blade templates
│   └── js/              # Frontend assets
├── routes/
│   ├── web.php
│   └── api.php
└── config/             # Configuration files
```

## Database Identification

### MySQL/MariaDB
- Configuration: `application.properties` with `jdbc:mysql://`
- ORM: Hibernate, JPA, Eloquent, Sequelize
- Files: `schema.sql`, `*.sql` migration files

### PostgreSQL
- Configuration: `jdbc:postgresql://`, `postgres://`
- ORM: Hibernate, TypeORM, Prisma

### MongoDB
- Configuration: `mongodb://`, `mongodb+srv://`
- ODM: Mongoose, Spring Data MongoDB

## Frontend Technologies

### JSP (JavaServer Pages)
- Files: `*.jsp` in `src/main/webapp/`
- Indicators: `<%@ page %>`, JSTL tags

### Thymeleaf
- Files: `*.html` in `src/main/resources/templates/`
- Indicators: `th:text`, `th:each` attributes

### React
- Files: `*.jsx`, `*.tsx`
- Indicators: `package.json` with `react` dependency

### Vue.js
- Files: `*.vue`
- Indicators: `package.json` with `vue` dependency

## Build Tools

### Maven (Java)
- File: `pom.xml`
- Commands: `mvn clean install`, `mvn spring-boot:run`

### Gradle (Java/Kotlin)
- Files: `build.gradle`, `build.gradle.kts`
- Commands: `./gradlew build`, `./gradlew bootRun`

### npm/yarn/pnpm (JavaScript)
- Files: `package.json`, `package-lock.json`, `yarn.lock`
- Commands: `npm install`, `npm run dev`

### Composer (PHP)
- Files: `composer.json`
- Commands: `composer install`

