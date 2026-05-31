import pickle
import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from .forms import PredictionForm
from .models import Prediction

BASE_DIR = settings.BASE_DIR
MODEL_DIR = os.path.join(BASE_DIR, "ml_model")
PIPELINE_PATH = os.path.join(MODEL_DIR, "full_pipeline.pkl")

def load_pipeline():
    with open(PIPELINE_PATH, "rb") as f:
        return pickle.load(f)

def dashboard(request):
    predictions = Prediction.objects.all().order_by("-created_at")
    total = predictions.count()
    positive = predictions.filter(result="Positive").count()
    negative = predictions.filter(result="Negative").count()

    age_dist = {}
    for p in predictions:
        bucket = (p.age // 10) * 10
        age_dist[bucket] = age_dist.get(bucket, 0) + 1
    age_labels = sorted(age_dist.keys())
    age_data = [age_dist[k] for k in age_labels]

    return render(request, "predictor/dashboard.html", {
        "total_predictions": total,
        "positive_count": positive,
        "negative_count": negative,
        "recent_predictions": predictions[:10],
        "age_labels": [f"{a}-{a+9}" for a in age_labels] if age_labels else ["No data"],
        "age_data": age_data or [0],
    })

def predict(request):
    result = None
    probability = None
    form = PredictionForm()

    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pipeline = load_pipeline()
            df = pd.DataFrame([data])
            prob = pipeline.predict_proba(df)[0, 1]
            pred = pipeline.predict(df)[0]

            result = "Positive" if pred == 1 else "Negative"
            probability = prob

            Prediction.objects.create(
                age=data["age"],
                sex=data["sex"],
                cp=data["cp"],
                trestbps=data["trestbps"],
                chol=data["chol"],
                fbs=data["fbs"],
                restecg=data["restecg"],
                thalch=data["thalch"],
                exang=data["exang"],
                oldpeak=data["oldpeak"],
                slope=data["slope"],
                ca=data["ca"],
                thal=data["thal"],
                result=result,
                probability=probability,
            )

    return render(request, "predictor/predict.html", {
        "form": form,
        "result": result,
        "probability": probability,
    })
