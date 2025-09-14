import gradio as gr
from real_vit import RealViTPredictor
import numpy as np

# Initialize predictor
predictor = RealViTPredictor()

def classify_image(image):
    """Classify uploaded image"""
    if image is None:
        return "Please upload an image"
    
    try:
        # Get predictions
        results = predictor.predict(image)
        
        # Format output
        output = "🎯 **Top 5 Predictions:**\n\n"
        for i, result in enumerate(results[:5]):
            confidence = result['percentage']
            class_name = result['class'].replace('_', ' ').title()
            
            # Add emoji for top prediction
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📍"
            output += f"{emoji} **{class_name}**: {confidence}\n"
        
        return output
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Custom CSS for better styling
css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
.output-markdown {
    font-size: 16px;
    line-height: 1.6;
}
"""

# Create Gradio interface
with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 20px;">
        <h1>🤖 Vision Transformer Image Classifier</h1>
        <p>Upload any image to get AI-powered classification using Vision Transformer (ViT-B/32)</p>
        <p><em>Trained on ImageNet with 1000+ categories</em></p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(
                type="pil",
                label="📸 Upload Image",
                height=400
            )
            
            classify_btn = gr.Button(
                "🔍 Classify Image", 
                variant="primary",
                size="lg"
            )
            
            gr.Examples(
                examples=[],
                inputs=image_input,
                label="💡 Try these examples:"
            )
        
        with gr.Column(scale=1):
            output = gr.Markdown(
                label="🎯 Predictions",
                value="Upload an image to see predictions...",
                elem_classes=["output-markdown"]
            )
            
            gr.HTML("""
            <div style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 10px;">
                <h3>📊 Model Information</h3>
                <ul>
                    <li><strong>Architecture:</strong> Vision Transformer (ViT-B/32)</li>
                    <li><strong>Parameters:</strong> ~86 million</li>
                    <li><strong>Training:</strong> ImageNet-1k</li>
                    <li><strong>Input Size:</strong> 224×224 pixels</li>
                </ul>
            </div>
            """)
    
    # Event handlers
    classify_btn.click(
        fn=classify_image,
        inputs=image_input,
        outputs=output
    )
    
    image_input.change(
        fn=classify_image,
        inputs=image_input,
        outputs=output
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()