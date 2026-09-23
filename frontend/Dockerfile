# Step 1: Use an official, lightweight Python blueprint as our starting baseline
FROM python:3.11-slim

# Step 2: Set the primary workspace directory inside the isolated container
WORKDIR /app

ENV PYTHONBUFFERED=1

# Step 3: Copy the dependency checklist file from our laptop into the container workspace
COPY requirements.txt /app/

# Step 4: Run the installer engine tool to download our Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy all remaining frontend application and HTML files into the workspace
COPY . /app/

# Step 6: Inform Docker that this container room listens for web traffic on Port 5000
EXPOSE 5000

# Step 7: The default runtime command executed the microsecond this box boots up
CMD ["python", "app.py"]
