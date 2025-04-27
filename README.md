FakeSnap – AI-Generated Image Detector
FakeSnap is a full-stack web application designed to detect AI-generated images by analyzing pixel-level features and statistical patterns. The project leverages machine learning and image processing to determine whether an image is real or fake, providing users with a reliable tool to distinguish between AI-generated and authentic images.

Features
Image Upload: Users can upload images to be analyzed.

AI Detection: The backend processes the images to detect whether they are AI-generated or real.

Results Display: The frontend displays the analysis results with clear indicators.

User-Friendly Interface: Simple and intuitive UI for easy interaction.

Full-Stack Implementation: Combines a Django backend with a React frontend for a seamless experience.

Tech Stack
Frontend: React, Vite

Backend: Django, Django REST Framework

Database: MySQL

Machine Learning: Python-based image analysis algorithms

Deployment: Docker, Podman for containerization

Setup
Prerequisites
Node.js and npm (for the frontend)

Python 3.10+ (for the backend)

MySQL (or a compatible database)

Frontend Setup
Navigate to the frontend directory:

bash
Copy
Edit
cd frontend
Install frontend dependencies:

bash
Copy
Edit
npm install
Run the frontend development server:

bash
Copy
Edit
npm run dev
The frontend will be available at http://localhost:5173.

Backend Setup
Navigate to the backend directory:

bash
Copy
Edit
cd backend
Set up a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
Install backend dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Apply migrations and create a superuser (for admin access):

bash
Copy
Edit
python manage.py migrate
python manage.py createsuperuser
Run the backend server:

bash
Copy
Edit
python manage.py runserver
The backend will be available at http://localhost:8000.

Docker Setup
To containerize both frontend and backend, ensure you have Docker and Podman installed.

Build the frontend Docker image:

bash
Copy
Edit
docker build -t fakesnap_frontend ./frontend
Build the backend Docker image:

bash
Copy
Edit
docker build -t fakesnap_backend ./backend
Run the containers:

bash
Copy
Edit
docker-compose up
This will run both the frontend and backend containers simultaneously.

Contributing
Contributions are welcome! If you want to improve the project, please follow these steps:

Fork the repository.

Create a new branch.

Make your changes.

Submit a pull request.

License
This project is licensed under the MIT License.
