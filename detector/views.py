from pathlib import Path

import numpy as np
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Card, CreditCardApplication, IssuedCard

MODEL_PATH = Path(settings.BASE_DIR) / "detector" / "ml_models" / "lstm_fraud_detection_model.h5"
_model = None
_model_loaded = False


def get_model():
    """Load the trained LSTM model once, when its file is available."""
    global _model, _model_loaded
    if _model_loaded:
        return _model
    _model_loaded = True
    if not MODEL_PATH.exists():
        return None
    try:
        from tensorflow.keras.models import load_model
        _model = load_model(MODEL_PATH)
    except Exception:
        _model = None
    return _model


def home(request):
    return render(request, "index.html", {})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        if not username:
            return render(request, "signup.html", {"error": "Username is required"})
        if not email or not password:
            return render(request, "signup.html", {"error": "Email and password are required"})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")
    return render(request, "signup.html", {})


def app_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password")
        return redirect("login")
    return render(request, "login.html", {})


def app_logout(request):
    logout(request)
    return redirect("home")


def prediction(request):
    result = None
    error = None
    if request.method == "POST":
        try:
            features = [
                float(request.POST.get("transaction_time", "")),
                float(request.POST.get("transaction_amount", "")),
                float(request.POST.get("cardholder_age", "")),
                float(request.POST.get("location_distance", "")),
            ]
            input_data = np.array([[features]], dtype=np.float32)
            model = get_model()
            if model is None:
                error = "Trained LSTM model not found. Add detector/ml_models/lstm_fraud_detection_model.h5."
            else:
                fraud_prediction = model.predict(input_data, verbose=0)
                result = (
                    "Fraudulent Transaction"
                    if float(np.asarray(fraud_prediction).reshape(-1)[0]) > 0.5
                    else "Legitimate Transaction"
                )
        except (TypeError, ValueError):
            error = "Please enter valid numeric values in all fields."
        except Exception:
            error = "Prediction failed. Please verify the trained model input shape."
    return render(request, "prediction.html", {
        "prediction_result": result,
        "error": error,
    })


def card_management(request):
    card = Card.objects.first()
    if request.method == "POST":
        if card is None:
            messages.error(request, "No card is available to manage.")
            return redirect("card_management")
        if "change_pin" in request.POST:
            new_pin = request.POST.get("new_pin", "")
            if new_pin and len(new_pin) == 4 and new_pin.isdigit():
                card.pin = new_pin
                card.save()
                messages.success(request, "Card PIN updated.")
            else:
                messages.error(request, "PIN must contain exactly four digits.")
        elif "toggle_lock" in request.POST:
            card.is_locked = not card.is_locked
            card.save()
            messages.success(request, "Card lock status updated.")
        elif "set_limits" in request.POST:
            card.domestic_limit_enabled = "domestic" in request.POST
            card.international_limit_enabled = "international" in request.POST
            card.save()
            messages.success(request, "Card limits updated.")
        return redirect("card_management")
    return render(request, "card_management.html", {"card": card})


def all(request):
    cards = Card.objects.all()
    return render(request, "all.html", {"cards": cards})


def apply_credit_card(request):
    if request.method == "POST":
        try:
            CreditCardApplication.objects.create(
                full_name=request.POST.get("full_name", "").strip(),
                age=int(request.POST.get("age", "")),
                email=request.POST.get("email", "").strip(),
                income=request.POST.get("income", ""),
            )
            messages.success(request, "Your credit-card application was submitted.")
            return redirect("application_status")
        except (TypeError, ValueError):
            messages.error(request, "Please enter valid application details.")
    return render(request, "apply_card.html")


def application_status(request):
    application = CreditCardApplication.objects.last()
    return render(request, "application_status.html", {
        "application": application,
        "is_approved": application.status == "Approved" if application else False,
    })


def approved_card(request):
    card = IssuedCard.objects.last()
    return render(request, "approved_card.html", {"card": card})


def all_applications(request):
    applications = CreditCardApplication.objects.all().order_by("-id")
    return render(request, "all_applications.html", {"applications": applications})
