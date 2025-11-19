FROM python:3.14-slim@sha256:119fd5bd9c01a9283d0be29d31218fb04f4575c67b3e89151417d61f6e1a6f58

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

CMD ["python", "./movarr.py"]
