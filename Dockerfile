FROM python:3.14-slim@sha256:fd2aff39e5a3ed23098108786a9966fb036fdeeedd487d5360e466bb2a84377b

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

CMD ["python", "./movarr.py"]
