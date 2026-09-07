FROM python:3.8-slim

# Install Java
RUN apt update && apt install -y openjdk-17-jre-headless curl bash procps

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH


# Set working directory
WORKDIR /pydev

# Copy files relative to workspace root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Spark job
CMD ["sleep", "infinity"]
