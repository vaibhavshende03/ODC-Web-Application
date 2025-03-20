
# **OBJECT DETECTION AND COUNTING**  

Object detection and counting play a crucial role in computer vision, with applications in surveillance, traffic management, and inventory monitoring. This web application leverages state-of-the-art deep learning techniques to perform real-time object detection and counting from live video feeds.  

Built using **Django** and **TensorFlow**, the system ensures high accuracy and efficiency. It features a user-friendly dashboard for visualizing detection results, along with secure user authentication. This application showcases the power of deep learning frameworks like TensorFlow in delivering scalable and effective solutions for object detection tasks.  

---

## 🚀 **Tech Stack**  
| Technology | Description |
|-----------|-------------|
| **Framework** | Django |
| **Deep Learning** | TensorFlow |
| **Frontend** | HTML, CSS |
| **Backend** | Python (Django) |

---

## 🌟 **Key Features**  
✅ **Real-Time Detection:** Detect objects from live video feeds with high accuracy.  
✅ **Object Counting:** Keep track of the number of detected objects in real time.  
✅ **User-Friendly Dashboard:** Intuitive interface for visualizing detection results.   

---

## 🖥️ **Screenshots**  

| Dashboard View | Detection in Action |  
|---------------|---------------------|  
| ![Screenshot 2025-02-20 152940](https://github.com/user-attachments/assets/6e37355d-fb2d-41cd-9ec8-779a86e5ebd5) | ![Screenshot 2025-02-20 200610](https://github.com/user-attachments/assets/a7fac35f-d9e0-4168-adc4-608610bb4c3b) |  

---

## 🔧 **Installation**  

### 1. **Clone the Repository**  
```bash
git clone https://github.com/vaibhavshende03/ODC-Web-Application.git
```

### 2. **Navigate to the Project Directory**  
```bash
cd your-repo
```

### 3. **Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 4. **Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## ⚙️ **Configuration**  

### 🔑 **Email Settings**  
Before running the project, update the **email settings** in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # 👉 Replace with your email  
EMAIL_HOST_PASSWORD = 'your-password'     # 👉 Replace with your password  
```

> **💡 Note:**  
> - If using Gmail, enable "Less secure apps" or create an "App Password" for security.  
> - For production, consider using environment variables to protect credentials.  

---

## 📊 **Database Setup**  

1. **Apply Migrations**  
```bash
python manage.py makemigrations  
python manage.py migrate  
```

2. **Create a Superuser** (Optional)  
```bash
python manage.py createsuperuser
```

---

## 🚀 **Run the Application**  
Start the development server:  
```bash
python manage.py runserver
```

Open your browser and visit:  
👉 `http://127.0.0.1:8000/`

---

## 🧠 **How It Works**  
1. The user logs into the application through a secure authentication system.  
2. The system receives a live video feed.  
3. TensorFlow processes the video feed to detect and count objects in real time.  
4. Results are displayed on a user-friendly dashboard.  

---

## 💡 **Troubleshooting**  
| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure all dependencies are installed using `pip install -r requirements.txt` |
| `ImportError: cannot import name` | Check the TensorFlow version compatibility |
| Email not sending | Enable "Less secure apps" or create an "App Password" for Gmail |

---

## 🤝 **Contributing**  
Contributions are welcome! If you'd like to contribute, follow these steps:  
1. Fork the repository.  
2. Create a new branch: `git checkout -b feature/your-feature`  
3. Commit your changes: `git commit -m 'Add new feature'`  
4. Push to the branch: `git push origin feature/your-feature`  
5. Open a pull request.  

---

## 📄 **License**  
This project is licensed under the [MIT License](LICENSE).  

---

## ⭐ **Show Your Support**  
If you found this project helpful, please consider giving it a ⭐ on GitHub!  

---
