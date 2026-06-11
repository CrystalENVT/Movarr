FROM python:3.14-slim@sha256:81ada6cb56bcbe3909644b4cb76ebe5354c65eaaad788a437bc1340a7638d49d

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

CMD ["python", "./movarr.py"]
