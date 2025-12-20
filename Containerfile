FROM python:3.14-alpine@sha256:7af51ebeb83610fb69d633d5c61a2efb87efa4caf66b59862d624bb6ef788345
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["bumpkin"]
