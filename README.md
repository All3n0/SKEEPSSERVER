# SKEEPSSERVER
# T-Shirt API

This is a Flask API application that provides endpoints for managing T-Shirts. The application uses a SQLite database to store T-Shirt data and allows users to create, retrieve, update, and delete T-Shirts.

## Features
- Create a new T-Shirt entry
- Retrieve a list of T-Shirt inspirations
- Retrieve T-Shirts by a specific inspiration category
- Update a T-Shirt entry
- Delete a T-Shirt entry
- Uses SQLite for persistent storage
- CORS enabled for cross-origin requests

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS

---

## **API Endpoints**

### **1. Create T-Shirt**
**URL:** `/tshirts`  
**Method:** `POST`

#### **Request Body:**
```json
{
  "name": "Graphic T-Shirt",
  "inspiration": "Graphic Design",
  "price": 30.00,
  "image": "tshirt1.jpg"
}
```

#### **Response:**
```json
{
  "message": "T-Shirt created successfully!",
  "tshirt_id": 1
}
```

---

### **2. Get T-Shirt Inspirations**
**URL:** `/tshirts`  
**Method:** `GET`

#### **Response:**
```json
[
  {
    "inspiration": "Graphic Design",
    "image": "graphic_tshirt.jpg"
  },
  {
    "inspiration": "Minimalist",
    "image": "minimalist_tshirt.jpg"
  }
]
```

---

### **3. Get T-Shirts by Inspiration**
**URL:** `/tshirts/inspiration/<string:inspiration>`  
**Method:** `GET`

#### **Response:**
```json
[
  {
    "id": 1,
    "name": "Graphic T-Shirt",
    "price": 30.00,
    "image": "tshirt1.jpg"
  },
  {
    "id": 2,
    "name": "Retro Graphic Tee",
    "price": 25.99,
    "image": "retro_tshirt.jpg"
  }
]
```

---

### **4. Update T-Shirt**
**URL:** `/tshirts/<int:tshirt_id>`  
**Method:** `PUT`

#### **Request Body:**
```json
{
  "name": "Updated T-Shirt Name",
  "price": 35.00,
  "image": "updated_tshirt.jpg"
}
```

#### **Response:**
```json
{
  "message": "T-Shirt updated successfully!"
}
```

---

### **5. Delete T-Shirt**
**URL:** `/tshirts/<int:tshirt_id>`  
**Method:** `DELETE`

#### **Response:**
```json
{
  "message": "T-Shirt deleted successfully!"
}
```

---

## **Database Schema**
The application uses a SQLite database to store T-Shirt data.

### **Tshirt Model**
| Field       | Type    | Description                      |
|------------|--------|----------------------------------|
| id         | Integer | Unique ID (Primary Key)        |
| name       | String  | Name of the T-Shirt            |
| inspiration | String  | Inspiration category           |
| price      | Float   | Price of the T-Shirt           |
| image      | String  | URL of the T-Shirt image       |

---

## **Setup and Installation**

### **Requirements**
Make sure you have Python installed on your system. Install the required dependencies using:
```bash
pip install Flask Flask-SQLAlchemy Flask-CORS
```

### **Running the Application**
Navigate to the project directory and run:
```bash
python app.py
```
This will start the Flask development server, and the application will be available at:
```
http://127.0.0.1:5000
```

---

## **Testing the Application**
You can use `curl` commands to test the API endpoints.

### **Create a new T-Shirt:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Graphic T-Shirt",
  "inspiration": "Graphic Design",
  "price": 30.00,
  "image": "tshirt1.jpg"
}' http://127.0.0.1:5000/tshirts
```

### **Get all T-Shirt inspirations:**
```bash
curl -X GET http://127.0.0.1:5000/tshirts
```

### **Get T-Shirts by inspiration:**
```bash
curl -X GET http://127.0.0.1:5000/tshirts/inspiration/Graphic%20Design
```

### **Update a T-Shirt:**
```bash
curl -X PUT -H "Content-Type: application/json" -d '{
  "name": "Updated Graphic Tee",
  "price": 35.99,
  "image": "updated_graphic_tshirt.jpg"
}' http://127.0.0.1:5000/tshirts/1
```

### **Delete a T-Shirt:**
```bash
curl -X DELETE http://127.0.0.1:5000/tshirts/1
```

---

## **License**
This project is licensed under the MIT License.

