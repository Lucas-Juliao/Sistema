# Flask Admin Dashboard

A modern and responsive admin dashboard built with Flask, using a professional and scalable project structure.

## Description

This project is a complete web system featuring a responsive sidebar, a clean and modern user interface, and a modular architecture using Flask Blueprints. It is designed to be a solid foundation for building complex web applications.

## Folder Structure

The project is organized using a structure that separates concerns, making it easy to maintain and scale:

```
/
|-- app/
|   |-- __init__.py         # Flask application factory
|   |-- routes/
|   |   `-- main.py         # Main application routes (Blueprint)
|   |-- static/
|   |   |-- css/
|   |   |   `-- style.css   # Main stylesheet
|   |   |-- js/
|   |   |   `-- script.js   # JavaScript for interactivity
|   |   `-- favicon.ico     # Application favicon
|   `-- templates/
|       |-- base.html       # Base template with sidebar and main layout
|       |-- dashboard.html  # Dashboard page template
|       |-- users.html      # Users page template
|       `-- settings.html   # Settings page template
|-- run.py                  # Main script to run the application
`-- README.md               # This file
```

## How to Run the Project

To run the project, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd <project-directory>
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install Flask Pillow
    ```

5.  **Run the application:**
    ```bash
    python run.py
    ```

The application will be available at `http://127.0.0.1:5000`.
