# Credit Card Fraud Detection

A Django final-year project based on the Python views and HTML pages supplied for this project.

## Main modules

- User signup and login
- Credit-card transaction fraud prediction form
- Card management: change PIN, lock/unlock card, domestic/international limits
- View all cards
- Credit-card application and application status
- Approved card view and all applications view

## Tech stack

- Python and Django
- SQLite (default Django database)
- NumPy and TensorFlow for the LSTM prediction model
- HTML, CSS and Bootstrap styling

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create an admin user if needed:

   ```bash
   python manage.py createsuperuser
   ```

6. Start Django:

   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/

## LSTM model required for real predictions

The supplied source had the model-loading line commented out, but called `model.predict()`.
That would cause a NameError. This project loads the model only if the file exists.

Copy your trained model to:

`detector/ml_models/lstm_fraud_detection_model.h5`

The model must accept the four input values in the same order as the prediction form:
transaction_time, transaction_amount, cardholder_age, location_distance.

If the model is absent, the prediction page displays a message that the model is not configured. It does not generate fake prediction results.

## Important reconstruction notes

This ZIP is organized from the code and HTML supplied in the chat. The original `models.py`, `urls.py`, remaining page templates, Techie theme asset folder, and trained `.h5` model were not supplied separately. The `Card`, `CreditCardApplication`, and `IssuedCard` models and the missing page templates have therefore been reconstructed from the fields and page names visible in the supplied views. Please compare these reconstructed parts with your original project before academic submission.
