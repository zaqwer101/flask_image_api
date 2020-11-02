# syntax=docker/dockerfile:experimental
FROM python:3.8-alpine
WORKDIR /api
ENV FLASK_APP api.py
ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
COPY api.py api.py
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
CMD ["flask", "run"]
