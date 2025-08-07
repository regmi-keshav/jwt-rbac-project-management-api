# FastAPI RBAC Project Management API

This is a **FastAPI** based backend that supports:
- User authentication with JWT
- Role-Based Access Control (RBAC)
- Project CRUD operations (Admin/User)
- Modular architecture using routers, services, and dependencies
- PostgreSQL with SQLModel

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/regmi-keshav/jwt-rbac-project-management-api.git
cd jwt-rbac-project-management-api
````

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root with the following content and update as needed:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/your_db"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 5. Run the App

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints



### Roles & Permissions

* **Admin**:

  * Can create, update, delete any project.
* **User**:

  * Can only view projects.

---


###  **AUTHENTICATION ENDPOINTS**

---

### **1. Register User**

* **Method**: `POST`
* **URL**: `/auth/register`
* **Headers**: None
* **Request Body**:

```json
{
  "username": "madmax",
  "password": "madmax@1",
  "role": "admin" // "user" or "admin"
}
```

* **Response**:

```json
{
  "id": 1,
  "username": "mr_saun",
  "role": "admin"
}
```

---

### **2. Login**

* **Method**: `POST`
* **URL**: `/auth/login`
* **Headers**: None
* **Request Body**:

```json
{
  "username": "madmax",
  "password": "madmax@1"
}
```

* **Response**:

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### **PROJECT ENDPOINTS (AUTH REQUIRED)**

All project endpoints require the `Authorization` header:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

### **3. Create Project (Admin Only)**

* **Method**: `POST`
* **URL**: `/projects/create`
* **Headers**:

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

* **Request Body**:

```json
{
  "name": "Project - Amazon Code",
  "description": "Initial Phase"
}
```

* **Response**:

```json
{
  "name": "Project - Amazon Code",
  "description": "Initial Phase",
  "id": 1,
  "owner_id": 1
}
```

---

### **4. Get All Projects (Any Authenticated User)**

* **Method**: `GET`
* **URL**: `/projects`
* **Headers**:

```http
Authorization: Bearer <JWT_TOKEN>
```

* **Response**:

```json
[
  {
    "name": "Project - Amazon Code",
    "description": "Initial Phase",
    "id": 1,
    "owner_id": 1
  },
  ...
]
```

---

### **5. Update Project (Admin Only)**

* **Method**: `PUT`
* **URL**: `/projects/{project_id}`
* **Headers**:

```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

* **Request Body**:

```json
{
  "name": "Project - Steerability",
  "description": "Phase 2"
}
```

* **Response**:

```json
{
  "name": "Project - Steerability",
  "description": "Phase 2",
  "id": 1,
  "owner_id": 1
}
```

---

### **6. Delete Project (Admin Only)**

* **Method**: `DELETE`
* **URL**: `/projects/{project_id}`
* **Headers**:

```http
Authorization: Bearer <JWT_TOKEN>
```

* **Response**:

```json
{
  "message": "Project deleted successfully"
}
```

---

## Notes

* Passwords are securely hashed using `bcrypt`.
* Role-based authorization is enforced via dependencies.
* Modular architecture separates concerns:

  * `api/`      → Business logic (service layer) for authentication and projects
  * `auth/`     → Auth logic and role dependencies
  * `db/`       → Database session and setup
  * `models/`   → SQLModel classes for database tables
  * `routes/`   → FastAPI routers (API endpoints)
  * `schemas/`  → Pydantic schemas
  * `config.py` → Settings like DB URL, JWT secret
  * `config.py` → Entry point
---