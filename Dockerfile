FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=123456
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=654321
COPY aline-schema.sql /docker-entrypoint-initdb.d
