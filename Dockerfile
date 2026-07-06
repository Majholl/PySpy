FROM docker.arvancloud.ir/python:3.14-slim AS builder

RUN apt-get update && apt-get upgrade && apt-get install --no-install-recommends -y \
   pkg-config \  
   build-essential \ 
   libpq-dev \  
   default-libmysqlclient-dev 

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt




FROM docker.arvancloud.ir/python:3.14-slim
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app

#  run apt-get upgrade later 
RUN apt-get update && apt-get upgrade && apt-get install --no-install-recommends -y \
   libmariadb3 \
   && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.14/site-packages/ /usr/local/lib/python3.14/site-packages/
# remove extra things from user local bin later
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser src .

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1 

USER appuser

EXPOSE 8000 

CMD ["fastapi", "run"]