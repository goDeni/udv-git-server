FROM registry.altlinux.org/alt/alt:p10

RUN \
    apt-get update \
    && apt-get install -y \
      fcgiwrap \
      git \
      nginx \
      python3 \
      spawn-fcgi

COPY server/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p --mode=0777 /var/log/nginx/ \
    && chmod 744 /etc/nginx/nginx.conf

VOLUME ["/git"]

CMD spawn-fcgi -M 0777 -s /tmp/fcgi.sock /usr/sbin/fcgiwrap && \
    nginx -g "daemon off;"