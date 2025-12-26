# Quick Start Guide

## 1. Installation (5 minutes)

### Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y cmake build-essential

# macOS
brew install cmake
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 2. Populate Your Face Store (2 minutes)

### Option A: From Individual Files
```python
from face_recognizer import FaceRecognizer

recognizer = FaceRecognizer()

# Add users
recognizer.add_user_face("alice.jpg", user_id=1, name="Alice Smith")
recognizer.add_user_face("bob.jpg", user_id=2, name="Bob Jones")
```

### Option B: From Database
Edit `migrate_database.py` with your database connection details and run it.

## 3. Start the Web Service (30 seconds)

```bash
python app.py
```

Server will start at `http://localhost:5000`

## 4. Test the API (1 minute)

### Add a face:
```bash
curl -X POST http://localhost:5000/api/v1/faces/add \
  -F "image=@user_photo.jpg" \
  -F "user_id=123" \
  -F "name=John Doe"
```

### Identify a face:
```bash
curl -X POST http://localhost:5000/api/v1/faces/identify \
  -F "image=@test_photo.jpg"
```

### Check health:
```bash
curl http://localhost:5000/health
```

## 5. Use in Your Code

```python
from face_recognizer import FaceRecognizer

recognizer = FaceRecognizer()

# Identify someone
result = recognizer.identify_user("unknown_person.jpg")

if result:
    print(f"User ID: {result['user_id']}")
    print(f"Confidence: {result['confidence']:.2%}")
else:
    print("User not found")
```

## Docker Deployment (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

## Troubleshooting

**Problem**: "No face detected"
- **Solution**: Use clear, front-facing photos with good lighting

**Problem**: Low confidence scores
- **Solution**: Lower the tolerance parameter (e.g., 0.5 instead of 0.6)

**Problem**: dlib installation fails
- **Solution**: Make sure cmake and build-essential are installed

## Next Steps

1. Review the full README.md for detailed documentation
2. Check out the API endpoints in the README
3. Customize the tolerance parameter for your use case
4. Set up production deployment with gunicorn

## Production Checklist

- [ ] Use gunicorn instead of Flask dev server
- [ ] Set up HTTPS/SSL
- [ ] Configure proper authentication
- [ ] Set up database backups for face_store.pkl
- [ ] Monitor API performance
- [ ] Set up logging
- [ ] Configure rate limiting
