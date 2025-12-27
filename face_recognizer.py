"""
Standalone Face Recognition Routine
Can be used independently without the web service
"""
from image_store import ImageStore
from typing import Optional, Dict


class FaceRecognizer:
    """
    Standalone face recognition class for easy integration
    """
    
    def __init__(self, store_path: str = "face_store.pkl"):
        """
        Initialize the face recognizer
        
        Args:
            store_path: Path to the face store file
        """
        self.store = ImageStore(store_path)
    
    def add_user_face(self, image_path: str, user_id: int, **metadata) -> bool:
        """
        Add a user's face to the recognition system
        
        Args:
            image_path: Path to the user's image file
            user_id: Unique identifier for the user
            **metadata: Additional metadata (name, email, etc.)
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> recognizer = FaceRecognizer()
            >>> recognizer.add_user_face("john.jpg", user_id=123, name="John Doe", email="john@example.com")
        """
        return self.store.add_image(
            image_path=image_path,
            user_id=user_id,
            metadata=metadata
        )
    
    def identify_user(self, image_path: str, tolerance: float = 0.6) -> Optional[Dict]:
        """
        Identify a user from an image
        
        Args:
            image_path: Path to the image to identify
            tolerance: Recognition tolerance (0.0-1.0, lower is stricter, default 0.6)
        
        Returns:
            Dict containing user_id and metadata if identified, None otherwise
        
        Example:
            >>> recognizer = FaceRecognizer()
            >>> result = recognizer.identify_user("unknown_person.jpg")
            >>> if result:
            ...     print(f"User ID: {result['user_id']}")
            ...     print(f"Confidence: {result['confidence']:.2%}")
        """
        return self.store.identify_face(image_path=image_path, tolerance=tolerance)
    
    def remove_user(self, user_id: int) -> bool:
        """
        Remove a user's face from the system
        
        Args:
            user_id: User ID to remove
        
        Returns:
            bool: True if removed, False if not found
        """
        return self.store.delete_by_user_id(user_id)
    
    def get_all_users(self) -> list:
        """
        Get all users in the system
        
        Returns:
            List of all user metadata
        """
        return self.store.get_all_metadata()


def main():
    """
    Example usage of the face recognition routine
    """
    # Initialize recognizer
    recognizer = FaceRecognizer()
    
    print("=" * 50)
    print("Face Recognition System - Example Usage")
    print("=" * 50)
    
    # Example 1: Add users to the system
    print("\n1. Adding users to the system...")
    
    # Note: You would replace these with actual image paths from your database
    # recognizer.add_user_face("path/to/user1.jpg", user_id=1, name="Alice Smith", email="alice@example.com")
    # recognizer.add_user_face("path/to/user2.jpg", user_id=2, name="Bob Jones", email="bob@example.com")
    
    print("   Users would be added from your database images here.")
    
    # Example 2: Identify a user from a new image
    print("\n2. Identifying a user from an image...")
    
    # Note: Replace with actual image path
    # result = recognizer.identify_user("path/to/unknown_person.jpg")
    # 
    # if result:
    #     print(f"   ✓ User identified!")
    #     print(f"   User ID: {result['user_id']}")
    #     print(f"   Confidence: {result['confidence']:.2%}")
    #     print(f"   Name: {result.get('name', 'N/A')}")
    #     print(f"   Email: {result.get('email', 'N/A')}")
    # else:
    #     print("   ✗ No matching user found")
    
    print("   User identification would happen here.")
    
    # Example 3: List all users
    print("\n3. Listing all users in the system...")
    all_users = recognizer.get_all_users()
    print(f"   Total users in system: {len(all_users)}")
    
    for i, user in enumerate(all_users, 1):
        print(f"   {i}. User ID: {user.get('user_id')}, Name: {user.get('name', 'N/A')}")
    
    # Example 4: Remove a user
    print("\n4. Removing a user...")
    # recognizer.remove_user(user_id=1)
    print("   User removal would happen here.")
    
    print("\n" + "=" * 50)
    print("Example complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
