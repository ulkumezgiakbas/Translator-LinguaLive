# Translator – LinguaLive 🌐

**Translator – LinguaLive** is a multi-language desktop translation app built with a PyWebView frontend and a Flask backend. It runs in a single native window, allowing instant translations without opening a browser.

## ✨ Features
- 🌐 **Multi-language translation** (real-time & on-demand)
- 🔊 **Text-to-Speech** (TTS) support
- 🪟 **Single native window** interface
- 📦 **One-click packaging** (.app / .exe)

## 🛠️ Technologies
- **Backend:** Python, Flask, WebSocket (flask-sock)
- **Frontend:** PyWebView, HTML, CSS, JavaScript
- **Extra:** gTTS or similar TTS libraries

## 🚀 Installation
1. Clone the repository:
   
   git clone https://github.com/ulkumezgiakbas/Translator-LinguaLive.git
   cd Translator-LinguaLive
   
2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate   # MacOS/Linux
   .venv\Scripts\activate      # Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Run the app:
    python run.py

Packaging as a Standalone App

Package into .exe or .app format using PyInstaller or similar tools:
pyinstaller --noconfirm --onefile --windowed run.py

License

This project is licensed under the MIT License.

<img width="1059" height="574" alt="Screenshot 2025-08-14 at 11 22 00" src="https://github.com/user-attachments/assets/b440c14c-f3c9-42d2-a514-d87663b3b9c3" />
