# Get the python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip uninstall -y setuptools wheel

# Copy the apps code
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the app via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

