FROM liquibase/liquibase:4.8.0

USER root

WORKDIR /app/

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends netcat postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY ./etc/migrator/wait-for.sh ./
COPY ./etc/migrator/entrypoint.sh ./entrypoint.sh
COPY ./etc/migrator/migrations ./migrations
COPY ./etc/migrator/fixtures ./fixtures

RUN chmod +x ./wait-for.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["update"]
