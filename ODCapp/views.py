import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import DetectedObject, Profile
from .forms import UserForm, ProfileForm
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

# Load the pre-trained model from TensorFlow Hub
MODEL_URL = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1"
MODEL_DIR = os.path.join('models/ssd_mobilenet_v2')

def load_model():
    try:
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        detector = hub.load(MODEL_URL)
        return detector
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

detector = load_model()

def load_labels(label_file):
    label_map = {}
    with open(label_file, 'r') as file:
        for line in file:
            class_id, label = line.strip().split(' ', 1)
            label_map[int(class_id)] = label
    return label_map

# Load the labels
label_map = load_labels("ODCapp/coco_labels.txt")

class VideoCamera(object):
    instance = None

    def __init__(self):
        if VideoCamera.instance is None:
            self.video = None
            self.detected_objects = {}
            self.alert_sent = False
            VideoCamera.instance = self

    def start_camera(self):
        if self.video is None or not self.video.isOpened():
            self.video = cv2.VideoCapture(0)

    def stop_camera(self):
        if self.video is not None and self.video.isOpened():
            self.video.release()
            self.video = None

    def get_frame(self):
        if self.video is None or not self.video.isOpened():
            return None

        success, image = self.video.read()
        if not success:
            return None

        # Prepare input tensor
        input_tensor = tf.convert_to_tensor(image, dtype=tf.uint8)[tf.newaxis, ...]

        # Run the model
        global detector
        if detector is None:
            detector = load_model()
            if detector is None:
                return None

        result = detector(input_tensor)
        result = {key: value.numpy() for key, value in result.items()}

        # Extract detection info
        boxes = result["detection_boxes"]
        scores = result["detection_scores"]
        classes = result["detection_classes"]

        # Draw boxes on the frame and update detected objects
        self.detected_objects = {}
        for i in range(len(boxes[0])):
            if scores[0][i] >= 0.5:
                class_id = int(classes[0][i])
                label = label_map.get(class_id, f"Class {class_id}")
                if label not in self.detected_objects:
                    self.detected_objects[label] = 0
                self.detected_objects[label] += 1
                box = boxes[0][i]
                x_min = int(box[1] * image.shape[1])
                y_min = int(box[0] * image.shape[0])
                x_max = int(box[3] * image.shape[1])
                y_max = int(box[2] * image.shape[0])
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                text = f"{label}: {scores[0][i]:.2f}"
                cv2.putText(image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw detected objects and their counts on the frame
        y_offset = 30
        for label, count in self.detected_objects.items():
            count_text = f"{label}: {count}"
            cv2.putText(image, count_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            y_offset += 30

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_detected_objects(self):
        return self.detected_objects

    def send_alert(self, object_label, user):
        email_subject = "Real-time Alert: Object Detected"
        email_body = f"A {object_label} has been detected by the camera."
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

# Singleton instance of the camera
camera = VideoCamera()

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def get_detected_objects(request):
    detected_objects = camera.get_detected_objects()
    return JsonResponse(detected_objects)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page after login
        else:
            return HttpResponse("Invalid username or password.")
    return render(request, 'login.html')
def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return HttpResponse("Your Password and Confirm Password do not match")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')  # Redirect to the login page after signup

    return render(request, 'signup.html')
@login_required
def indexPage(request):
    camera.start_camera()
    return render(request, 'index.html')

def leave_index_page(request):
    camera.stop_camera()
    return HttpResponse("Camera stopped")

def logout_view(request):
    if request.user.is_authenticated:
        # Get the detected objects before logging out
        detected_objects = camera.get_detected_objects()

        # Prepare the email content
        email_subject = "Object Detection Summary"
        email_body = "Here is the summary of detected objects during your session:\n\n"
        for label, count in detected_objects.items():
            email_body += f"{label}: {count}\n"

        # Send the email
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

        # Shut down the camera
        camera.stop_camera()

        # Log out the user
        logout(request)

    return redirect('login')

@login_required
def dashboard(request):
    detected_objects = DetectedObject.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'detected_objects': detected_objects
    }
    return render(request, 'dashboard.html', context)

from django.contrib import messages

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)