

YatraAI is a prototype tourism platform designed to help travelers plan personalized, budget-aware, and day-wise travel itineraries across Incredible India. It leverages a custom Python weighted recommendation scoring model, Gemini AI LLM integration (with seamless local offline fallback), itemized budget estimation, and interactive Leaflet.js OpenStreetMap routing.

---

## Key Features

1. **Visually Impressive Indian Tourism Landing Page**:
   - Modern travel UI featuring popular destinations, category filters, and hidden gem spotlights.
2. **Search & Filter Tourism Discovery**:
   - Filter 40+ pre-seeded Indian tourist spots by state, city, category, budget, duration, and interests.
3. **Personalized Preference Engine**:
   - Multi-attribute questionnaire capturing origin, destination, days (1–15), budget (₹), travel companions (Solo, Couple, Family, Friends), travel pace, and multi-select interests.
4. **Weighted Recommendation Engine**:
   - Evaluates candidate places using weighted scoring: Interest Match (35%), Budget Compatibility (20%), Duration Compatibility (15%), Destination Relevance (15%), Travel Type (10%), and Rating (5%).
5. **AI Day-Wise Itinerary Generation**:
   - Gemini LLM structures day-by-day schedules (Morning, Afternoon, Evening) with activity descriptions, entry costs, and travel tips.
6. **Robust Offline Fallback Engine**:
   - If the AI API key is unconfigured or network is unavailable during a live hackathon demo, the system automatically switches to an offline rule-based itinerary generator so the presentation never fails.
7. **Itemized Budget Analysis**:
   - Categorizes costs into Accommodation, Transport, Food, Activities, and Miscellaneous, providing budget status badges and cost-reduction suggestions.
8. **Interactive Leaflet.js Route Map**:
   - Displays destination markers, custom popup details, and sequential polyline route paths.
9. **Saved Trips & User Authentication**:
   - Built-in Django Auth allowing registered users to save, view, and delete itineraries.
10. **CSV Data Importer & Django Admin**:
    - Includes management command `python manage.py import_places` to seed sample destinations from `data/tourist_places.csv`.

---

## Tech Stack

- **Backend**: Python 3.14, Django 6.0, Django REST Framework
- **Database**: SQLite3 (Development / Prototype), PostgreSQL compatible model schema
- **AI Integration**: Gemini API (`google-genai` SDK) + Python Fallback Rule Engine
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, FontAwesome 6
- **Maps**: Leaflet.js & OpenStreetMap API

---

## Installation & Setup Instructions

### 1. Clone & Setup Workspace
Navigate to the project root directory:
```powershell
cd c:\Users\ASUS\Desktop\sih
```

### 2. Install Required Packages
```powershell
python -m pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Edit `.env` to supply your Gemini API key (Optional; if left blank, offline fallback mode activates automatically):
```env
SECRET_KEY=django-insecure-sih-yatra-ai-key-prototype-2026
DEBUG=True
AI_API_KEY=your_gemini_api_key_here
```

### 4. Database Setup & Migration
Run Django migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Import Sample Tourism Dataset
Seed database with 40+ curated Indian tourist destinations from CSV:
```powershell
python manage.py import_places
```

### 6. Create Superuser (Admin Access)
```powershell
python manage.py createsuperuser
```

### 7. Run Local Development Server
```powershell
python manage.py runserver
```
Open your browser at `http://127.0.0.1:8000/`.

## Deploy to Vercel

The Django app runs as a Vercel Function. Vercel's filesystem is temporary, so
configure a persistent PostgreSQL database before deploying; the app deliberately
does not run migrations inside web requests.

1. In Vercel, import `VenkateshR16/Smart_Tour_Assistant` and keep the **Root
   Directory** set to the repository root (the folder containing `manage.py`).
   Leave the Framework Preset on **Django** or **Other**; the repository's
   `vercel.json` builds the React frontend and Vercel detects Django from
   `manage.py`.
2. Add a PostgreSQL database through Vercel Marketplace (for example, Neon) and
   connect it to this Vercel project. Confirm the project has a `DATABASE_URL`
   environment variable. The PostgreSQL driver is included in `requirements.txt`.
3. In **Settings → Environment Variables**, set:
   - `SECRET_KEY`: a new, random Django secret (do not reuse the example key).
     Generate one locally with `python -c "import secrets; print(secrets.token_urlsafe(50))"`
     and paste the output into Vercel; do not commit it.
   - `DEBUG`: `False`.
   - `DATABASE_URL`: supplied by your connected PostgreSQL provider.
   - `GEMINI_API_KEY`: optional; without it, itinerary generation uses the
     offline fallback.
   - `ALLOWED_HOSTS`: optional for a custom domain, as a comma-separated list
     (for example, `.vercel.app,your-domain.example`).
   - `CSRF_TRUSTED_ORIGINS`: optional for a custom domain, including the scheme
     (for example, `https://your-domain.example`).
4. Deploy from the Vercel dashboard. The build command in `vercel.json` installs
   frontend dependencies and builds `frontend/dist`; Django serves the API and
   Vercel collects and serves Django static files.
5. Initialize the database once from a terminal with the Vercel CLI installed
   and linked to this project:

   ```powershell
   npx vercel login
   npx vercel link
   npx vercel env pull .env.local
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py import_places
   ```

   `.env.local` is ignored by Git. To administer users, create a superuser with
   `python manage.py createsuperuser` after migrations.

After setup, future pushes to the connected GitHub branch trigger deployments.
Database migrations should be run explicitly when the schema changes.

---

## Prototype Demonstration Flow (For SIH Judges)

To present the full working end-to-end prototype flow:

1. Open **Home Page** (`http://127.0.0.1:8000/`).
2. Click **Plan My Trip** (or click the quick demo button).
3. Enter preferences:
   - **Origin**: `New Delhi`
   - **Destination**: `Rajasthan`
   - **Number of Days**: `4`
   - **Budget**: `₹15,000`
   - **Travel Group**: `Friends`
   - **Interests**: `History`, `Culture`, `Food`
4. Click **Create My Trip**.
5. View **Personalized Recommendations** sorted by match score percentage with rationale tags.
6. Click **Generate AI Itinerary**.
7. Review the generated **4-Day Itinerary** broken down into Morning, Afternoon, and Evening slots.
8. Inspect the **Itemized Budget Gauge** showing Stay, Transport, Food, Entry fees vs ₹15,000 limit.
9. Interact with the **Leaflet Route Map** showing numbered markers and polyline route paths for Jaipur, Amer Fort, Jodhpur, and Pushkar.
10. Click **Save Trip** (Register/Login user) and verify saved trip appears under **My Trips**.

---

## Important System Files

- **Recommendation Engine**: `tourism/services/recommendation.py`
- **AI & Fallback Itinerary Service**: `tourism/services/ai_service.py`
- **Budget Estimator**: `tourism/services/budget_service.py`
- **Database Models**: `tourism/models.py`
- **CSV Importer Command**: `tourism/management/commands/import_places.py`
- **Map Script**: `static/js/map.js`

---

## Future Scope

- Real-time hotel and transport API integrations (IRCTC, MakeMyTrip, Skypicker).
- OpenWeather API weather-aware adaptive itinerary replanning.
- Multilingual voice travel assistant for Indian regional languages.
- Crowd-density analytics and real-time hidden gem recommendations.
