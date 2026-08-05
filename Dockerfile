FROM python:3.14-slim@sha256:7bec7ddcddeff7975d6ba9b4be7dd6f6b2f55e7491539145e2978f7f97ce9144

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

CMD ["python", "./movarr.py"]
