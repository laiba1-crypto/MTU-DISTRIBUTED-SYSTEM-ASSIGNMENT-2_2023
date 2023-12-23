FROM python:3.8-slim

# Assign the container's working directory.
WORKDIR /app

# Copy the locally stored files to the container.
COPY . /app/

COPY requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8888 available
EXPOSE 8888

RUN pwd && ls -la

# Launch the s.py script as the container starts.
CMD ["python", "./s.py"]
