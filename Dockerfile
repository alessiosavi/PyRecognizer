# FROM python:latest
FROM alessiosavi/python-alpine-dlib:v0.0.3

RUN apk add git gcc g++ openblas-dev openblas openblas-static lapack-dev lapack blas-dev blas zlib-dev zlib jpeg-dev jpeg linux-headers

# The latest alpine images don't have some tools like (`git` and `bash`).
# Adding git, bash and openssh to the image

#RUN apk add make g++ gcc cmake binutils
# RUN apt update && apt upgrade -y && apt install -y cmake build-essential libatlas-base-dev liblapack-dev

LABEL maintainer="Alessio Savi <alessiosavibtc@gmail.com>"

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy the source from the current directory to the Working Directory inside the container
COPY . /app

RUN pip download -d .pipcache -r requirements.txt

RUN pip install -r requirements.txt

RUN apk del git gcc g++ openblas-dev openblas openblas-static lapack-dev lapack blas-dev blas zlib-dev zlib jpeg-dev jpeg linux-headers
# Expose port 8081 to the outside world
EXPOSE 8081

# Run the executable
CMD ["python", "main.py"]
