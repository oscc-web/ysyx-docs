# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y curl gnupg python3 python3-pip && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify Node.js and npm installation
RUN node -v && npm -v

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json, package-lock.json, and requirements.txt
COPY package*.json requirements.txt ./

# Install Node.js dependencies
RUN npm install

# Install Python dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Expose the port on which your application will run
EXPOSE 3000

# Set the default command to bash for interactive use
CMD ["/bin/bash"]
