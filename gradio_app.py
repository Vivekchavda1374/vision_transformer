import gradio as gr
from real_vit import RealViTPredictor
import logging

# Initialize predictor
predictor = RealViTPredictor()

def predict_image(image):
    """Predict image classification"""
    try:
        if image is None:
            return "Please upload an image"
        
        # Make prediction
        results = predictor.predict(image)
        
        # Format results
        output = []
        for i, result in enumerate(results[:5]):
            confidence = f"{result['percentage']}"
            output.append(f"{i+1}. {result['class']}: {confidence}")
        
        return "\n".join(output)
    
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(type="pil"),
    outputs=gr.Textbox(label="Top 5 Predictions"),
    title="🤖 Vision Transformer Image Classifier",
    description="Upload an image to get AI-powered classification using Vision Transformer (ViT-B/32)",
    examples=None,
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()