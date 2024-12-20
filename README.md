# MathMind: Handwritten Math Problem Solver

MathMind is an interactive web application that allows users to draw mathematical equations and problems directly on their screen and receive instant solutions. Powered by Django, HTMX, and Google's Gemini API, it combines the convenience of natural handwriting with powerful AI problem-solving capabilities.

## ✨ Features

### 📝 Drawing Interface
- Intuitive drawing canvas for writing mathematical equations
- Touch-screen and stylus support for better precision
- Clear and reset canvas options
- Adjustable pen thickness and color options

### 🧮 Math Recognition & Solving
- Real-time recognition of handwritten mathematical expressions
- Step-by-step solution explanations
- Support for various types of math problems:
  - Basic arithmetic
  - Algebraic equations
  - Calculus problems
  - Geometric calculations
  - Word problems

### ⚡ Real-time Interaction
- Instant processing using HTMX
- No page refreshes needed
- Seamless integration between drawing and results

## 🚀 Technology Stack

- **Backend Framework**: Django
- **Frontend Enhancement**: HTMX
- **Drawing Interface**: HTML Canvas
- **AI Integration**: Google Gemini API
- **Math Processing**: Flask API Integration

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Modern web browser with JavaScript enabled

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mathmind
cd mathmind
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit `http://localhost:8000` in your browser

## 🎯 Usage

1. **Draw Your Problem**
   - Use your mouse, touch, or stylus to write your math problem
   - Utilize the toolbar for different drawing options
   - Click "Clear" to start over

2. **Get Solutions**
   - Click "Solve" to process your handwritten problem
   - View the recognized equation and step-by-step solution
   - Save or share your results

## 🔧 Configuration

### Required Environment Variables
```
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_django_secret_key
```

### Optional Settings
```python
# settings.py
DRAWING_CANVAS_SIZE = {
    'width': 800,
    'height': 400
}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes:
```bash
git commit -m 'Add some AmazingFeature'
```
4. Push to the branch:
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

## 🔍 Troubleshooting

Common issues and solutions:

1. **Drawing Not Registering**
   - Ensure JavaScript is enabled
   - Check browser compatibility
   - Try clearing browser cache

2. **API Connection Issues**
   - Verify API key is correctly set
   - Check internet connection
   - Confirm API service status

## 📘 API Documentation

### Gemini API Integration
```python
# Example API call structure
response = gemini.generate_content(
    "Solve and explain: [processed_image_data]"
)
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django community
- HTMX creators
- Google Gemini team
- Open-source contributors
- Math education community

## 📞 Support

For support, please:
1. Check the [Issues](https://github.com/yourusername/mathmind/issues) page
2. Create a new issue if needed
3. Join our [Discord community](your-discord-link)

