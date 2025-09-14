# Vision Transformer Web Application

A beautiful web interface for image classification using Google's Vision Transformer (ViT) model, built with Flask and modern web technologies.

## Features

- 🖼️ **Drag & Drop Image Upload** - Easy image uploading with visual feedback
- 🤖 **Vision Transformer Model** - Powered by Google's ViT architecture
- 📊 **Real-time Predictions** - Get top-5 classification results instantly
- 🎨 **Modern UI/UX** - Beautiful, responsive design with animations
- 📱 **Mobile Friendly** - Works seamlessly on all devices
- ⚡ **Fast Processing** - Optimized for quick inference

## Architecture

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **ML Framework**: JAX/Flax
- **Model**: Vision Transformer (ViT-B/32)

## Installation

1. **Clone the repository**
   ```bash
   cd /home/vivek/Applications/genai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload an Image**
   - Drag and drop an image onto the upload area
   - Or click "Choose File" to select an image
   - Supported formats: JPG, PNG, GIF, WebP

2. **View Results**
   - See the uploaded image preview
   - Get top-5 classification predictions with confidence scores
   - View model information and architecture details

3. **API Endpoints**
   - `GET /` - Main web interface
   - `POST /predict` - Image classification endpoint
   - `GET /health` - Health check
   - `GET /model-info` - Model information

## API Usage

### Predict Endpoint

```bash
curl -X POST -F "image=@your_image.jpg" http://localhost:5000/predict
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "class": "golden_retriever",
      "confidence": 0.85,
      "percentage": "85.00%"
    }
  ],
  "image": "data:image/png;base64,iVBOR...",
  "model_info": {
    "name": "Vision Transformer (ViT-B/32)",
    "architecture": "Transformer-based",
    "input_size": "224x224",
    "parameters": "86M"
  }
}
```

## Model Information

- **Architecture**: Vision Transformer (ViT-B/32)
- **Input Size**: 224×224 pixels
- **Parameters**: ~86 million
- **Training Data**: ImageNet-21k (pre-training) + ImageNet-1k (fine-tuning)
- **Paper**: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"

## File Structure

```
genai/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── js/
│       └── script.js     # JavaScript functionality
└── vision_transformer-main/  # ViT model code
    └── vit_jax/          # JAX implementation
```

## Features Explained

### Vision Transformer Architecture
- **Patch Embedding**: Images are divided into 16×16 patches
- **Position Encoding**: Learnable position embeddings for spatial awareness
- **Multi-Head Attention**: Self-attention mechanism for global context
- **MLP Blocks**: Feed-forward networks for feature transformation

### Web Interface Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload experience
- **Real-time Feedback**: Loading states and error handling
- **Smooth Animations**: Enhanced user experience with CSS transitions
- **Accessibility**: Keyboard shortcuts and screen reader support

## Keyboard Shortcuts

- `Ctrl/Cmd + U`: Open file upload dialog
- `Escape`: Close error notifications

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Performance

- **Image Processing**: ~100-500ms per image
- **Model Inference**: Depends on hardware (CPU/GPU)
- **File Size Limit**: 10MB per image
- **Supported Formats**: JPEG, PNG, GIF, WebP

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **JAX Installation Issues**
   ```bash
   pip install --upgrade jax jaxlib
   ```

3. **Memory Issues**
   - Reduce image size before upload
   - Ensure sufficient RAM (4GB+ recommended)

### Development Mode

Run with debug mode for development:
```bash
export FLASK_ENV=development
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the original Vision Transformer repository for details.

## Acknowledgments

- Google Research for the Vision Transformer model
- JAX/Flax team for the ML framework
- Flask community for the web framework

## Citation

If you use this code in your research, please cite:

```bibtex
@article{dosovitskiy2020image,
  title={An image is worth 16x16 words: Transformers for image recognition at scale},
  author={Dosovitskiy, Alexey and Beyer, Lucas and Kolesnikov, Alexander and Weissenborn, Dirk and Zhai, Xiaohua and Unterthiner, Thomas and Dehghani, Mostafa and Minderer, Matthias and Heigold, Georg and Gelly, Sylvain and others},
  journal={arXiv preprint arXiv:2010.11929},
  year={2020}
}
```