from django import forms

WIDGET = forms.Select(attrs={"class": "form-control"})
TEXT_WIDGET = forms.NumberInput(attrs={"class": "form-control"})

class PredictionForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=1, max_value=120, widget=TEXT_WIDGET)
    sex = forms.ChoiceField(label="Sex", choices=[("Male", "Male"), ("Female", "Female")], widget=WIDGET)
    cp = forms.ChoiceField(
        label="Chest Pain Type",
        choices=[
            ("typical angina", "Typical Angina"),
            ("atypical angina", "Atypical Angina"),
            ("non-anginal", "Non-anginal Pain"),
            ("asymptomatic", "Asymptomatic"),
        ],
        widget=WIDGET,
    )
    trestbps = forms.IntegerField(label="Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, widget=TEXT_WIDGET)
    chol = forms.IntegerField(label="Serum Cholesterol (mg/dl)", min_value=50, max_value=600, widget=TEXT_WIDGET)
    fbs = forms.ChoiceField(label="Fasting Blood Sugar > 120 mg/dl", choices=[("TRUE", "Yes"), ("FALSE", "No")], widget=WIDGET)
    restecg = forms.ChoiceField(
        label="Resting ECG",
        choices=[
            ("normal", "Normal"),
            ("lv hypertrophy", "LV Hypertrophy"),
            ("st-t abnormality", "ST-T Abnormality"),
        ],
        widget=WIDGET,
    )
    thalch = forms.IntegerField(label="Max Heart Rate Achieved", min_value=30, max_value=250, widget=TEXT_WIDGET)
    exang = forms.ChoiceField(label="Exercise Induced Angina", choices=[("TRUE", "Yes"), ("FALSE", "No")], widget=WIDGET)
    oldpeak = forms.FloatField(label="ST Depression Induced by Exercise", min_value=0.0, max_value=10.0, widget=TEXT_WIDGET)
    slope = forms.ChoiceField(
        label="Peak Exercise ST Segment",
        choices=[("upsloping", "Upsloping"), ("flat", "Flat"), ("downsloping", "Downsloping")],
        widget=WIDGET,
    )
    ca = forms.IntegerField(label="Number of Major Vessels (0-4)", min_value=0, max_value=4, widget=TEXT_WIDGET)
    thal = forms.ChoiceField(
        label="Thalassemia",
        choices=[("normal", "Normal"), ("fixed defect", "Fixed Defect"), ("reversable defect", "Reversible Defect")],
        widget=WIDGET,
    )
