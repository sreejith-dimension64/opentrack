# Face Recognition Web Service

A complete Python-based face recognition system with REST API for identifying users from images.

## Features

- **Face Recognition**: Identify users from uploaded images
- **Persistent Storage**: Store face encodings and metadata in a pickle file
- **REST API**: Flask-based web service with multiple endpoints
- **Flexible Integration**: Standalone Python module or web service
- **Database Migration**: Scripts to populate from existing RDBMS

## System Requirements

- Python 3.7+
- dlib (face_recognition dependency)
- CMake (for building dlib)

### Installing System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y cmake build-essential
```

**macOS:**
```bash
brew install cmake
```

**Windows:**
- Install Visual Studio Build Tools
- Install CMake from https://cmake.org/download/

## Installation

1. Clone or download this project

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

Note: Installing `face_recognition` may take a few minutes as it compiles dlib.

## Quick Start

### Option 1: Standalone Python Usage

```python
from face_recognizer import FaceRecognizer

# Initialize
recognizer = FaceRecognizer()

# Add a user
recognizer.add_user_face(
    "path/to/user_photo.jpg", 
    user_id=123, 
    name="John Doe",
    email="john@example.com"
)

# Identify a user
result = recognizer.identify_user("path/to/unknown_photo.jpg")

if result:
    print(f"User ID: {result['user_id']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Name: {result.get('name')}")
```

### Option 2: Web Service

1. Start the Flask server:
```bash
python app.py
```

2. The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Face Recognition API",
  "faces_in_store": 5
}
```

### 2. Add Face
```bash
POST /api/v1/faces/add
```

**Form Data:**
- `image`: Image file (jpg/jpeg/png)
- `user_id`: User ID (required)
- Additional fields: name, email, etc. (optional)

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/faces/add \
  -F "image=@user_photo.jpg" \
  -F "user_id=123" \
  -F "name=John Doe" \
  -F "email=john@example.com"
```

**Response:**
```json
{
  "success": true,
  "message": "Face added successfully",
  "user_id": 123,
  "metadata": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### 3. Identify Face
```bash
POST /api/v1/faces/identify
```

**Form Data:**
- `image`: Image file (jpg/jpeg/png)
- `tolerance`: Recognition tolerance (optional, default 0.6)

**Example:**
```bash
curl -X POST http://localhost:5000/api/v1/faces/identify \
  -F "image=@unknown_person.jpg" \
  -F "tolerance=0.6"
```

**Response (if identified):**
```json
{
  "identified": true,
  "user_id": 123,
  "confidence": 0.85,
  "distance": 0.15,
  "metadata": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Response (if not identified):**
```json
{
  "identified": false,
  "message": "No matching face found"
}
```

### 4. List All Faces
```bash
GET /api/v1/faces
```

**Response:**
```json
{
  "count": 2,
  "faces": [
    {
      "user_id": 123,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "user_id": 456,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ]
}
```

### 5. Delete Face
```bash
DELETE /api/v1/faces/<user_id>
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/v1/faces/123
```

### 6. Clear Store
```bash
POST /api/v1/faces/clear
```

## Migrating from Database

Use the `migrate_database.py` script to populate the face store from your existing database:

### From PostgreSQL:
```python
import psycopg2
from image_store import ImageStore

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="your_db",
    user="your_user",
    password="your_password"
)

cursor = conn.cursor()
store = ImageStore()

# Query images
cursor.execute("SELECT user_id, image_blob, name FROM users")

for user_id, image_data, name in cursor:
    store.add_image(
        image_bytes=image_data,
        user_id=user_id,
        metadata={'name': name}
    )
```

### From Filesystem:
```python
from image_store import ImageStore

store = ImageStore()

user_mapping = {
    'user_001.jpg': {'user_id': 1, 'name': 'Alice'},
    'user_002.jpg': {'user_id': 2, 'name': 'Bob'},
}

for filename, data in user_mapping.items():
    store.add_image(
        image_path=f'./images/{filename}',
        user_id=data['user_id'],
        metadata={'name': data['name']}
    )
```

## Configuration

### Tolerance Parameter
Controls how strict face matching is:
- **0.6** (default): Balanced - works well for most cases
- **0.5**: Stricter - fewer false positives
- **0.7**: More lenient - more matches but potential false positives

### File Locations
- **Face Store**: `face_store.pkl` (can be changed in initialization)
- **Uploads**: `uploads/` directory (for web service)

## Production Deployment

For production use, replace Flask's development server with a production WSGI server:

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker:
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## How It Works

1. **Face Encoding**: Each face is converted to a 128-dimensional vector using deep learning
2. **Storage**: Encodings are stored in a pickle file with associated metadata
3. **Identification**: New faces are compared using Euclidean distance
4. **Matching**: If distance is below tolerance threshold, face is identified

## Performance

- **Add Face**: ~1-2 seconds per image
- **Identify**: ~0.5-1 seconds with 100 stored faces
- **Storage**: ~1KB per face encoding

## Limitations

- Works best with clear, front-facing photos
- Lighting conditions can affect accuracy
- Multiple faces in one image: uses first detected face
- Very similar looking people may be confused

## Troubleshooting

**"No face detected":**
- Ensure image has a clear, visible face
- Check image quality and lighting
- Try a different photo

**"dlib installation failed":**
- Install system dependencies (cmake, build-essential)
- Try: `pip install dlib` separately
- On Windows, use pre-built wheels

**Low confidence scores:**
- Adjust tolerance parameter
- Use higher quality reference images
- Ensure consistent lighting/angles

## Project Structure

```
.
├── app.py                  # Flask web service
├── face_recognizer.py      # Standalone face recognition class
├── image_store.py          # Core storage and recognition logic
├── migrate_database.py     # Database migration scripts
├── requirements.txt        # Python dependencies
├── face_store.pkl          # Face encodings storage (created at runtime)
└── uploads/               # Temporary upload directory
```

## License

This project uses the `face_recognition` library which is built on dlib and is licensed under MIT.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API examples
3. Check face_recognition documentation: https://github.com/ageitgey/face_recognition
