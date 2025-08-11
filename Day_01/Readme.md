🎯 Day 01 – Initial Project Setup
This project is the starting point for the 30 Days of Voice Agents Challenge. On Day 1, we established the core foundation for a web application, setting up a simple backend with FastAPI and a basic frontend with HTML and JavaScript.

🧠 What We Built
This repository contains a simple web application that demonstrates the basic setup of a Python backend and a web-based frontend.

Backend: A FastAPI server that serves a static HTML file at the root endpoint (/).

Frontend: An index.html file that links to an external JavaScript file (script.js).

File Serving: The FastAPI server is configured to serve static assets (like CSS and JavaScript) from a static directory.

🛠 Tech Stack
Backend:

FastAPI

Jinja2 (for HTML templating)

uvicorn (ASGI server)

Frontend:

HTML

JavaScript

📂 Project Structure
.
├── main.py               # FastAPI backend logic
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # The main HTML page
└── static/
    └── js/
        └── script.js     # Frontend JavaScript
🚀 Getting Started
Follow these steps to set up and run the project locally.

1. Clone the Repository
Bash

git clone <your-repository-url>
cd <your-project-folder>
2. Install Dependencies
First, ensure you have Python and pip installed. Then, install the required libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
3. Run the Application
Start the FastAPI server using uvicorn. The --reload flag is useful for development as it automatically restarts the server on code changes.

Bash

uvicorn main:app --reload
4. Verify the Setup
Open your web browser and navigate to http://localhost:8000.

You should see the text: "Welcome to My Web App!"

To confirm the JavaScript is being served correctly, open your browser's developer console (F12 or Cmd+Option+I on Mac) and check the "Console" tab. You should see the message: "Hello from script.js! The backend is serving this file."