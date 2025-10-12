# Use Python 3.10 base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Expose port 8000 (checker will detect this)
EXPOSE 8000

# Run the Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
