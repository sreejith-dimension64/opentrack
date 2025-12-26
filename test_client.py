"""
Test Client for Face Recognition Web Service
Demonstrates how to interact with the API
"""
import requests
import json


class FaceRecognitionClient:
    """
    Client for interacting with the Face Recognition API
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def add_face(self, image_path: str, user_id: int, **metadata):
        """
        Add a face to the system
        
        Args:
            image_path: Path to image file
            user_id: User ID
            **metadata: Additional metadata (name, email, etc.)
        
        Returns:
            API response
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'user_id': user_id, **metadata}
            
            response = requests.post(
                f"{self.base_url}/api/v1/faces/add",
                files=files,
                data=data
            )
        
        return response.json()
    
    def identify_face(self, image_path: str, tolerance: float = 0.6):
        """
        Identify a face
        
        Args:
            image_path: Path to image file
            tolerance: Recognition tolerance
        
        Returns:
            API response
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'tolerance': tolerance}
            
            response = requests.post(
                f"{self.base_url}/api/v1/faces/identify",
                files=files,
                data=data
            )
        
        return response.json()
    
    def list_faces(self):
        """List all faces in the system"""
        response = requests.get(f"{self.base_url}/api/v1/faces")
        return response.json()
    
    def delete_face(self, user_id: int):
        """
        Delete a face
        
        Args:
            user_id: User ID to delete
        
        Returns:
            API response
        """
        response = requests.delete(f"{self.base_url}/api/v1/faces/{user_id}")
        return response.json()
    
    def clear_store(self):
        """Clear all faces from the store"""
        response = requests.post(f"{self.base_url}/api/v1/faces/clear")
        return response.json()


def main():
    """
    Example usage of the test client
    """
    # Initialize client
    client = FaceRecognitionClient()
    
    print("=" * 60)
    print("Face Recognition API - Test Client")
    print("=" * 60)
    
    # 1. Health check
    print("\n1. Health Check")
    print("-" * 60)
    try:
        health = client.health_check()
        print(json.dumps(health, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API server is running: python app.py")
        return
    
    # 2. List current faces
    print("\n2. Listing Current Faces")
    print("-" * 60)
    try:
        faces = client.list_faces()
        print(json.dumps(faces, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Add a face (example - you need actual image files)
    print("\n3. Adding a Face (Example)")
    print("-" * 60)
    print("To add a face, use:")
    print("  result = client.add_face('path/to/image.jpg', user_id=123, name='John Doe')")
    print("  print(json.dumps(result, indent=2))")
    
    # Example (uncomment if you have test images):
    # try:
    #     result = client.add_face(
    #         'test_image.jpg',
    #         user_id=1,
    #         name='Test User',
    #         email='test@example.com'
    #     )
    #     print(json.dumps(result, indent=2))
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # 4. Identify a face (example - you need actual image files)
    print("\n4. Identifying a Face (Example)")
    print("-" * 60)
    print("To identify a face, use:")
    print("  result = client.identify_face('path/to/unknown.jpg', tolerance=0.6)")
    print("  print(json.dumps(result, indent=2))")
    
    # Example (uncomment if you have test images):
    # try:
    #     result = client.identify_face('unknown_person.jpg', tolerance=0.6)
    #     print(json.dumps(result, indent=2))
    #     
    #     if result.get('identified'):
    #         print(f"\n✓ Identified as User ID: {result['user_id']}")
    #         print(f"  Confidence: {result['confidence']:.2%}")
    #     else:
    #         print("\n✗ No matching face found")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # 5. Delete a face (example)
    print("\n5. Deleting a Face (Example)")
    print("-" * 60)
    print("To delete a face, use:")
    print("  result = client.delete_face(user_id=123)")
    print("  print(json.dumps(result, indent=2))")
    
    print("\n" + "=" * 60)
    print("Test client examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
