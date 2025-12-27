"""
Face Recognition Web Service
Flask-based REST API for face identification
"""
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from image_store import ImageStore
from migrate_database import example_sqlserver
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1,
    x_port=1,
    x_prefix=1
)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize image store
image_store = ImageStore(store_path='face_store.pkl')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Face Recognition API',
        'faces_in_store': len(image_store.face_encodings)
    }), 200


@app.route('/api/v1/faces/add', methods=['POST'])
def add_face():
    """
    Add a new face to the store
    
    Form Data:
        - image: Image file (jpg/jpeg/png)
        - user_id: User ID (required)
        - name: User name (optional)
        - email: User email (optional)
        - any other metadata fields
    
    Returns:
        JSON response with success status
    """
    try:
        # Check if image is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        # Get user_id
        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({'error': 'user_id must be an integer'}), 400
        
        # Collect all metadata from form
        metadata = {}
        for key, value in request.form.items():
            if key != 'user_id':
                metadata[key] = value
        
        # Read image bytes
        image_bytes = file.read()
        
        # Add to store
        success = image_store.add_image(
            image_bytes=image_bytes,
            user_id=user_id,
            metadata=metadata
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Face added successfully',
                'user_id': user_id,
                'metadata': metadata
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add face. No face detected in image.'
            }), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/v1/faces/identify', methods=['POST'])
def identify_face():
    """
    Identify a face from the store
    
    Form Data:
        - image: Image file (jpg/jpeg/png)
        - tolerance: Recognition tolerance (optional, default 0.6, lower is stricter)
    
    Returns:
        JSON response with user metadata if identified
    """
    try:
        # Check if image is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        # Get tolerance parameter
        tolerance = request.form.get('tolerance', '0.6')
        try:
            tolerance = float(tolerance)
        except ValueError:
            return jsonify({'error': 'tolerance must be a number'}), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Identify face
        result = image_store.identify_face(
            image_bytes=image_bytes,
            tolerance=tolerance
        )
        
        if result:
            return jsonify({
                'identified': True,
                'user_id': result.get('user_id'),
                'confidence': result.get('confidence'),
                'distance': result.get('distance'),
                'metadata': {k: v for k, v in result.items() 
                           if k not in ['user_id', 'confidence', 'distance']}
            }), 200
        else:
            return jsonify({
                'identified': False,
                'message': 'No matching face found'
            }), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/v1/faces', methods=['GET'])
def list_faces():
    """
    List all faces in the store
    
    Returns:
        JSON array of all metadata
    """
    try:
        all_metadata = image_store.get_all_metadata()
        print(f"Listing {len(all_metadata)} faces in store")
        return jsonify({
            'count': len(all_metadata),
            'faces': all_metadata
        }), 200
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/v1/faces/<int:user_id>', methods=['DELETE'])
def delete_face(user_id):
    """
    Delete a face by user_id
    
    Args:
        user_id: User ID to delete
    
    Returns:
        JSON response with success status
    """
    try:
        success = image_store.delete_by_user_id(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Deleted face(s) for user_id: {user_id}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No face found for user_id: {user_id}'
            }), 404
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/v1/faces/clear', methods=['POST'])
def clear_store():
    """
    Clear all faces from the store (use with caution!)
    
    Returns:
        JSON response with success status
    """
    try:
        image_store.clear_store()
        return jsonify({
            'success': True,
            'message': 'All faces cleared from store'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    
@app.route('/api/v1/storedb', methods=['POST'])
def store_database():
    example_sqlserver()
    return jsonify({
        'success': True,
        'message': 'Database migration executed'
    }), 200

@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
