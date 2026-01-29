FROM python:3.14-alpine@sha256:59d996ce35d58cbe39f14572e37443a1dcbcaf6842a117bc0950d164c38434f9
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["bumpkin"]
