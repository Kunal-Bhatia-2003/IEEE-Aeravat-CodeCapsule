import pickle
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import YourModel  # Import your Django model

# Load the trained model
with open('path_to_your_pickled_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a function to preprocess input data and make predictions
def predict_fraud(request):
    if request.method == 'POST':
        # Get input data from the request
        features = request.POST.dict()  # Assuming features are passed as key-value pairs
        features.pop('csrfmiddlewaretoken', None)  # Remove CSRF token if present
        data = [float(features[key]) for key in features]  # Convert data to float if necessary

        # Make prediction
        prediction = model.predict(np.array([data]))

        # Convert prediction to human-readable format
        if prediction[0] == "No Fraud":
            result = "No Fraud Detected"
        else:
            result = "Fraud Detected"

        # Return prediction as JSON response
        return JsonResponse({'result': result})

    else:
        return JsonResponse({'error': 'Invalid request method'})