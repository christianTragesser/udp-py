FROM python:3-alpine

RUN addgroup -S -g 2222 udp && \
    adduser -S -u 2222 -g udp udp && \
    mkdir /opt
    
COPY receiver.py /opt/

RUN chmod 755 -R /opt

USER udp

EXPOSE 5000

CMD ["/bin/sh", "-c", "python /opt/receiver.py"]