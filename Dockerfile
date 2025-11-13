FROM python:3.14-slim

WORKDIR /app

# This should be able to stay static normally,
#   so do this first for docker layering
COPY ./requirements.txt /app/
RUN pip install --root-user-action ignore -r requirements.txt

# Do this next, as sometimes this won't change (automatic builds, etc)
COPY ./movarr.py /app/
COPY ./functions/* /app/functions/

ENV DEBIAN_FRONTEND="noninteractive"
# This will always run, so do this near the end
RUN apt-get update && \
    apt-get install -y --no-install-recommends tini && \
    rm -rf /var/lib/apt/lists/*

# Use tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python3", "/app/movarr.py"]
