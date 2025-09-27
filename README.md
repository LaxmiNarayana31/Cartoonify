# Cartoonify: Image to Cartoon Avatar Generator

Cartoonify is a simple web application that transforms your face images into cartoon-style avatars with transparent backgrounds. Built with [Streamlit](https://streamlit.io/), [OpenCV](https://opencv.org/), and [MediaPipe](https://mediapipe.dev/), it provides a fun and easy way to create cartoon avatars from your photos.

---

## Features

- Upload a face image (JPG, JPEG, PNG)
- Automatic face detection and validation
- Cartoon effect with edge-preserving smoothing
- Background removal for transparent PNG avatars
- Download your generated cartoon avatar

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/LaxmiNarayana31/Cartoonify.git
cd Cartoonify
```

### 2. Install [uv](https://github.com/astral-sh/uv) (if not already installed)

```bash
pip install uv
```

### 3. Create and activate a virtual environment using uv

```bash
uv venv
# On Windows (PowerShell):
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 4. Install dependencies with uv

```bash
uv sync
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

- `app.py` &mdash; Main Streamlit application
- `pyproject.toml` &mdash; Project dependencies (managed by uv)
- `uploads/` &mdash; Folder for uploaded images (auto-created)
- `avatars/` &mdash; Output folder for generated cartoon avatars (auto-created)

---

## How it Works

1. **Upload**: Select a face image (min. 512x512 px recommended)
2. **Face Detection**: Ensures a clear face is present
3. **Cartoonify**: Applies bilateral filtering and edge detection for a cartoon effect
4. **Background Removal**: Uses MediaPipe Selfie Segmentation for transparent background
5. **Download**: Preview and download your cartoon avatar as a PNG

---

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management

---
