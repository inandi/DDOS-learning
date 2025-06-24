# Use an official Python runtime as a parent image
# Lightweight Python image
FROM python:3.9-slim-buster  

# Set the working directory in the container
# All following commands run in /app
WORKDIR /app  

# Copy the current directory contents into the container at /app
# Copy app code into the container
COPY . /app  

# Install Flask and Gunicorn (production WSGI server)
RUN pip install flask gunicorn  # Install dependencies

# --- REMOVE THIS LINE: ---
# RUN echo "net.ipv4.tcp_max_syn_backlog = 8" >> /etc/sysctl.conf && sysctl -p

# Expose port 80 to allow traffic to the web server
# The app will listen on port 80
EXPOSE 80  

# Run the Flask app with Gunicorn, 1 worker, and a very low backlog (2)
# This makes the server easy to overwhelm for DDOS demonstration
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:80", "--backlog", "2", "app:app"]