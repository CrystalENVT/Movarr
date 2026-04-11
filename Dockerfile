FROM python:3.14-slim@sha256:bc389f7dfcb21413e72a28f491985326994795e34d2b86c8ae2f417b4e7818aa

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

CMD ["python", "./movarr.py"]
