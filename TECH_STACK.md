# Tech Stack: Blood Group Classification Project

This document outlines the technologies, libraries, and frameworks used in this project.

## Frontend

*   **Framework:** React
*   **Build Tool:** Vite
*   **Language:** JavaScript (JSX)
*   **HTTP Client:** Axios
*   **Styling:**
    *   Tailwind CSS (inferred from `tailwind-merge` and `clsx`)
*   **UI Components:**
    *   `lucide-react` (for icons)
    *   `framer-motion` (for animations)

## Backend

*   **Language:** Python
*   **Framework:** Flask
*   **Web Server Gateway Interface:** Werkzeug (part of Flask)
*   **CORS Handling:** Flask-CORS

## Machine Learning & Data Processing

*   **Core ML Framework:** TensorFlow
*   **High-Level API:** Keras (bundled with TensorFlow)
*   **Scientific Computing:**
    *   NumPy
    *   SciPy
*   **Image Processing:**
    *   OpenCV (`opencv-python`)
    *   Pillow (`PIL`)
*   **Data Analysis (potential use):** Pandas
*   **Machine Learning Utilities:** Scikit-learn

## Database

The application uses a hybrid database strategy for resilience:
*   **Primary Database:** MongoDB (via `pymongo`)
*   **Fallback Database:** SQLite (built-in Python `sqlite3` module)

## Tooling & Utilities

*   **Environment Variables:** `python-dotenv`
*   **Package Management:**
    *   `pip` (Python)
    *   `npm` (Node.js/Frontend)
*   **Date/Time Handling:** `python-dateutil`
*   **Binary Data Handling:** `h5py` (for reading `.keras` model files)
