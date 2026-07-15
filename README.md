# Trekking Management Application (TMA)

Trekking Management Application (TMA) is a web application that allows Admins, Trek Staff, and Users (Trekkers) to manage and coordinate trek registrations, slot availability, and bookings based on their roles.

---

### 1. Prerequisites
Ensure you have the following installed on your local machine:
* Python 3.10+
* NodeJS (v18+) & npm
* Redis Server
* MailHog (or any local SMTP server listening on port 1025)

---

### Backend Setup
1. Navigate to the backend directory and set up a Python virtual environment:
   ```bash
   cd backend
   python3 -m venv .env
   source .env/bin/activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirement.txt
   ```
   * Password : Admin (`admin@admin.com` / `admin@admin.com`)

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```

---

## Running the Services

To run the full Trekking Management Application, start the following services in separate terminal sessions:

### 1. Redis Server (Cache & Celery Broker)
Start your local Redis instance:
```bash
redis-server
```

### 2. Flask Backend API
Activate the virtual environment and start the development server:
```bash
cd backend
source .env/bin/activate
python app.py
```
* The API will be available at `http://127.0.0.1:5000`.

### 3. Celery Worker (Async Tasks)
Run the Celery worker to handle background tasks (welcome emails, CSV exports):
```bash
cd backend
source .env/bin/activate
celery -A celery_app.celeryApp worker --loglevel=info
```

### 4. Celery Beat (Scheduled Reminders & Reports)
Run Celery Beat to trigger scheduled jobs:
```bash
cd backend
source .env/bin/activate
celery -A celery_app.celeryApp beat --loglevel=info
```

### 5. MailHog (SMTP Tester)
Start MailHog to capture emails sent by Celery tasks:
```bash
mailhog
```
* Access the MailHog web interface to view captured emails: `http://localhost:8025`.

### 6. Vue Frontend (UI Client)
Start the Vite development server:
```bash
cd frontend
npm run dev
```
* The user interface will be accessible at `http://localhost:5173`.

---

## Celery Tasks & Scheduled Jobs

The application includes periodic background tasks managed by Celery Beat:
1. **Daily Reminder (`daily_reminder`):** Sends emails to users whose treks start tomorrow. Runs daily at 8:00 AM (configured in `celery_app.py`).
2. **Monthly Activity Report (`monthly_reminder`):** Generates an HTML trekking activity report for Admin. Runs on the 2nd of every month at 4:30 PM (configured in `celery_app.py`).

### Manually Triggering Celery Tasks (For Testing/Debugging)
You can trigger these tasks manually (either synchronously for debugging, or asynchronously via the worker) using Python command-line commands. Make sure your virtual environment is active and you are in the `backend` folder:

* **Manually trigger Daily Reminders:**
  * *Synchronous execution (outputs directly to your terminal):*
    ```bash
    python3 -c "from celery_app import daily_reminder; daily_reminder()"
    ```
  * *Asynchronous execution (sends job to Celery worker):*
    ```bash
    python3 -c "from celery_app import daily_reminder; daily_reminder.delay()"
    ```

* **Manually trigger Monthly Reports:**
  * *Synchronous execution (outputs directly to your terminal):*
    ```bash
    python3 -c "from celery_app import monthly_reminder; monthly_reminder()"
    ```
  * *Asynchronous execution (sends job to Celery worker):*
    ```bash
    python3 -c "from celery_app import monthly_reminder; monthly_reminder.delay()"
    ```

---

## Caching & Redis Commands

The application uses Redis database `2` for API caching. You can monitor and view cache data using `redis-cli`:

* **Monitor commands in real-time:**
  ```bash
  redis-cli -n 2 monitor
  ```
* **View all active cache keys:**
  ```bash
  redis-cli -n 2 keys "*"
  ```
* **Fetch and read deserialized cache data:**
  ```bash
  python3 -c "import redis, pickle; r = redis.Redis(db=2); print(pickle.loads(r.get('YOUR_CACHE_KEY')))"
  ```
* **Flush/Clear the cache manually:**
  ```bash
  redis-cli -n 2 flushdb
  ```

---