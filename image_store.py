"""
Image Store Module
Handles storage and retrieval of face encodings and user metadata
"""
import pickle
import os
import face_recognition
import numpy as np
from typing import Optional, Dict, List, Tuple
from PIL import Image
import io


class ImageStore:
    """
    Store for face encodings and associated metadata
    """
    
    def __init__(self, store_path: str = "face_store.pkl"):
        """
        Initialize the image store
        
        Args:
            store_path: Path to the pickle file for storing face data
        """
        self.store_path = store_path
        self.face_encodings: List[np.ndarray] = []
        self.metadata: List[Dict] = []
        self.load_store()
    
    def load_store(self):
        """Load existing face encodings and metadata from disk"""
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, 'rb') as f:
                    data = pickle.load(f)
                    self.face_encodings = data.get('encodings', [])
                    self.metadata = data.get('metadata', [])
                print(f"Loaded {len(self.face_encodings)} face encodings from store")
            except Exception as e:
                print(f"Error loading store: {e}")
                self.face_encodings = []
                self.metadata = []
        else:
            print("No existing store found. Starting fresh.")
    
    def save_store(self):
        """Save face encodings and metadata to disk"""
        try:
            data = {
                'encodings': self.face_encodings,
                'metadata': self.metadata
            }
            with open(self.store_path, 'wb') as f:
                pickle.dump(data, f)
            print(f"Saved {len(self.face_encodings)} face encodings to store")
        except Exception as e:
            print(f"Error saving store: {e}")
            raise
    
    def add_image(self, image_path: str = None, image_bytes: bytes = None, 
                  user_id: int = None, metadata: Dict = None) -> bool:
        """
        Add a new face image to the store
        
        Args:
            image_path: Path to image file (optional if image_bytes provided)
            image_bytes: Image as bytes (optional if image_path provided)
            user_id: User ID to associate with the face
            metadata: Additional metadata dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load image
            if image_path:
                image = face_recognition.load_image_file(image_path)
            elif image_bytes:
                pil_image = Image.open(io.BytesIO(image_bytes))
                image = np.array(pil_image)
            else:
                raise ValueError("Either image_path or image_bytes must be provided")
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                print("No face detected in the image")
                return False
            
            if len(face_encodings) > 1:
                print(f"Multiple faces detected ({len(face_encodings)}). Using the first one.")
            
            # Store the first face encoding
            face_encoding = face_encodings[0]
            
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            if user_id is not None:
                metadata['user_id'] = user_id
            
            # Add to store
            self.face_encodings.append(face_encoding)
            self.metadata.append(metadata)
            
            # Save to disk
            self.save_store()
            
            print(f"Added face for user_id: {user_id}")
            return True
            
        except Exception as e:
            print(f"Error adding image: {e}")
            return False
    
    def identify_face(self, image_path: str = None, image_bytes: bytes = None, 
                     tolerance: float = 0.6) -> Optional[Dict]:
        """
        Identify a face from the store
        
        Args:
            image_path: Path to image file (optional if image_bytes provided)
            image_bytes: Image as bytes (optional if image_path provided)
            tolerance: How much distance between faces to consider it a match (lower is stricter)
            
        Returns:
            Dict with metadata if face is identified, None otherwise
        """
        try:
            # Load image
            if image_path:
                image = face_recognition.load_image_file(image_path)
            elif image_bytes:
                pil_image = Image.open(io.BytesIO(image_bytes))
                image = np.array(pil_image)
            else:
                raise ValueError("Either image_path or image_bytes must be provided")
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                print("No face detected in the image")
                return None
            
            if len(face_encodings) > 1:
                print(f"Multiple faces detected ({len(face_encodings)}). Using the first one.")
            
            unknown_encoding = face_encodings[0]
            
            # If store is empty
            if len(self.face_encodings) == 0:
                print("Store is empty. No faces to compare against.")
                return None
            
            # Compare with all stored faces
            matches = face_recognition.compare_faces(
                self.face_encodings, 
                unknown_encoding, 
                tolerance=tolerance
            )
            
            # Calculate face distances
            face_distances = face_recognition.face_distance(
                self.face_encodings, 
                unknown_encoding
            )
            
            # Find the best match
            if True in matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    match_metadata = self.metadata[best_match_index].copy()
                    match_metadata['confidence'] = float(1 - face_distances[best_match_index])
                    match_metadata['distance'] = float(face_distances[best_match_index])
                    print(f"Face identified: {match_metadata}")
                    return match_metadata
            
            print("No matching face found in store")
            return None
            
        except Exception as e:
            print(f"Error identifying face: {e}")
            return None
    
    def get_all_metadata(self) -> List[Dict]:
        """Get all stored metadata"""
        return self.metadata.copy()
    
    def delete_by_user_id(self, user_id: int) -> bool:
        """
        Delete a face from the store by user_id
        
        Args:
            user_id: User ID to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        indices_to_delete = []
        for i, meta in enumerate(self.metadata):
            if meta.get('user_id') == user_id:
                indices_to_delete.append(i)
        
        if not indices_to_delete:
            return False
        
        # Delete in reverse order to maintain indices
        for i in sorted(indices_to_delete, reverse=True):
            del self.face_encodings[i]
            del self.metadata[i]
        
        self.save_store()
        print(f"Deleted {len(indices_to_delete)} face(s) for user_id: {user_id}")
        return True
    
    def clear_store(self):
        """Clear all data from the store"""
        self.face_encodings = []
        self.metadata = []
        self.save_store()
        print("Store cleared")
