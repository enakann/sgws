# Use the standard Nginx image from Docker Hub
FROM nginx

ENV HOME=/opt/repo

# install python, uwsgi, and supervisord
RUN apt-get update && apt-get install -y supervisor uwsgi python3 python3-pip procps vim 
RUN /usr/bin/pip3 install uwsgi flask flask_restful

RUN rm -rf /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python

# Source code file
COPY ./storage_grid ${HOME}/storage_grid

RUN pip3 install -r ${HOME}/storage_grid/requirements.txt
# Copy the configuration file from the current directory and paste 
# it inside the container to use it as Nginx's default config.
COPY ./deployment/nginx.conf /etc/nginx/nginx.conf


# setup NGINX config
RUN mkdir -p /spool/nginx /run/pid && \
    chmod -R 777 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chgrp -R 0 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    rm /etc/nginx/conf.d/default.conf

RUN apt-get install -y wget

ARG GOSU_VERSION=1.10
RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
 && wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch" \
 && chmod +x /usr/local/bin/gosu \
 && gosu nobody true


# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./deployment/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

COPY ./deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN touch /var/log/supervisor/supervisord.log

EXPOSE 8080:8080

# setup entrypoint
COPY ./deployment/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# access to /dev/stdout
# https://github.com/moby/moby/issues/31243#issuecomment-406879017
RUN ln -s /usr/local/bin/docker-entrypoint.sh / && \
    chmod 777 /usr/local/bin/docker-entrypoint.sh && \
    chgrp -R 0 /usr/local/bin/docker-entrypoint.sh && \
    chown -R nginx:root /usr/local/bin/docker-entrypoint.sh

# https://docs.openshift.com/container-platform/3.3/creating_images/guidelines.html
RUN chgrp -R 0 /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
    chmod -R g+rwX /var/log /var/cache /run/pid /spool/nginx /var/run /run /tmp /etc/uwsgi /etc/nginx && \
    chown -R nginx:root ${HOME} && \
    chmod -R 777 ${HOME} /etc/passwd

# enter
WORKDIR ${HOME}
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["supervisord"]
