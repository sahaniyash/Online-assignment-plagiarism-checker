FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY . .

# Expose the port the Flask app will run on
EXPOSE 5000

# Run the Python backend application
CMD ["python", "app.py"]
