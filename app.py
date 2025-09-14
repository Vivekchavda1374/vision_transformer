from flask import Flask, request, jsonify, render_template
from PIL import Image
import io
import base64
import logging
from real_vit import RealViTPredictor

app = Flask(__name__)
predictor = RealViTPredictor()



@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image prediction requests"""
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Validate file size (max 10MB)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:
            return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 400
        
        # Read and process image
        try:
            image = Image.open(file.stream)
        except Exception as e:
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Make prediction
        predictions = predictor.predict(image)
        
        # Convert image to base64 for display
        img_buffer = io.BytesIO()
        # Resize for display (max 512px)
        display_size = min(512, max(image.size))
        display_image = image.copy()
        display_image.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)
        display_image.save(img_buffer, format='PNG', optimize=True)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'image': f'data:image/png;base64,{img_str}',
            'model_info': {
                'name': 'Vision Transformer (ViT-B/32)',
                'architecture': 'Transformer-based',
                'input_size': '224x224',
                'parameters': '86M',
                'patch_size': '32x32',
                'num_classes': len(predictor.classes)
            }
        })
        
    except Exception as e:
        logging.error(f"Prediction endpoint error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': predictor.model is not None
    })

@app.route('/model-info')
def model_info():
    """Get detailed model information"""
    info = {
        'model_name': 'Vision Transformer (ViT-B/32)',
        'description': 'A Vision Transformer model for image classification',
        'input_size': [224, 224, 3],
        'num_classes': len(predictor.classes),
        'architecture': 'Transformer',
        'paper': 'An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale',
        'patch_size': [32, 32],
        'hidden_size': 768,
        'num_layers': 12,
        'num_heads': 12,
        'mlp_dim': 3072
    }
    

    
    return jsonify(info)



if __name__ == '__main__':
    import os
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)