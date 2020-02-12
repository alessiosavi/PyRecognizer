FROM python:latest

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image
RUN apt update && apt upgrade -y && apt install -y cmake build-essential libatlas-base-dev liblapack-dev

LABEL maintainer="Alessio Savi <alessiosavibtc@gmail.com>"

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy the source from the current directory to the Working Directory inside the container
COPY . /app

RUN pip install -r requirements.txt

# Expose port 8081 to the outside world
EXPOSE 8081

# Run the executable
CMD ["python", "main.py"]