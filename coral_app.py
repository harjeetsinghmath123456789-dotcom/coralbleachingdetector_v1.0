# coral_app.py
import pickle
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

class CoralDetectorApp:
    def __init__(self, root):
        self.root = root
        root.title("Coral Bleaching Detector")
        root.geometry("500x600")
        root.configure(bg='#f0f0f0')
        
        # Try to load model
        self.model = None
        self.load_model()
        
        # Create UI
        self.create_widgets()
    
    def load_model(self):
        """Load the model from various possible locations"""
        possible_paths = [
            'coral_model.pkl',
            'coral_model_clean.pkl', 
            'Coral Bleaching Detection.pkcls',
            os.path.join(os.path.dirname(sys.argv[0]), 'coral_model.pkl'),
            os.path.join(os.path.dirname(sys.argv[0]), 'Coral Bleaching Detection.pkcls')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        model = pickle.load(f)
                    
                    # Extract if it's Orange wrapper
                    if hasattr(model, 'model'):
                        self.model = model.model
                    else:
                        self.model = model
                    
                    print(f"Loaded model from: {path}")
                    print(f"Model type: {type(self.model).__name__}")
                    print(f"Features needed: {self.model.n_features_in_}")
                    return
                except:
                    continue
        
        self.model = None
        print("No model found. Please ensure model file is in the same folder.")
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="🪸 Coral Bleaching Detector", 
                         font=("Arial", 20, "bold"), bg='#f0f0f0')
        title.pack(pady=20)
        
        # Subtitle
        subtitle = tk.Label(self.root, text="Upload a coral image to detect bleaching",
                           font=("Arial", 12), bg='#f0f0f0')
        subtitle.pack(pady=5)
        
        # Select button
        self.btn_select = tk.Button(self.root, text="📸 Select Coral Image", 
                                    command=self.select_image,
                                    font=("Arial", 14), bg='#4CAF50', fg='white',
                                    padx=20, pady=10)
        self.btn_select.pack(pady=30)
        
        # Image preview
        self.image_label = tk.Label(self.root, bg='#f0f0f0')
        self.image_label.pack(pady=10)
        
        # Result frame
        self.result_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.result_frame.pack(pady=20)
        
        self.result_label = tk.Label(self.result_frame, text="", 
                                     font=("Arial", 18, "bold"), bg='#f0f0f0')
        self.result_label.pack()
        
        self.confidence_label = tk.Label(self.result_frame, text="",
                                         font=("Arial", 12), bg='#f0f0f0')
        self.confidence_label.pack()
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                     font=("Arial", 10), bg='#ddd', relief='sunken')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Coral Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if not file_path:
            return
        
        self.status_label.config(text=f"Processing: {os.path.basename(file_path)}")
        self.root.update()
        
        # Show preview
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        from PIL import ImageTk
        photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
        # Make prediction
        result, confidence = self.predict(file_path)
        
        if result == 1:
            self.result_label.config(text="⚠️ BLEACHED DETECTED", fg='red')
        else:
            self.result_label.config(text="✅ HEALTHY CORAL", fg='green')
        
        self.confidence_label.config(text=f"Confidence: {confidence:.1f}%")
        self.status_label.config(text=f"Completed: {os.path.basename(file_path)}")
    
    def predict(self, image_path):
        """Simple prediction - you'll need to add the embedding code"""
        # For now, return random result
        # We'll add the actual embedding code next
        import random
        return random.choice([0, 1]), random.uniform(70, 99)
        
        # TODO: Add SqueezeNet embedding here

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CoralDetectorApp(root)
    root.mainloop()