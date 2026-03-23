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

# Create a non-root user and give it ownership of the app directory
RUN useradd -r -s /bin/false appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the app via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

