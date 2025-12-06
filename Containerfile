FROM python:3.14-alpine@sha256:b80c82b1a282283bd3e3cd3c6a4c895d56d1385879c8c82fa673e9eb4d6d4aa5
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["bumpkin"]
