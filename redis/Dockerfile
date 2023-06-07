FROM redis

COPY redis_data.txt /

ENTRYPOINT nohup bash -c "redis-server --appendonly yes" \
	& sleep 5s \
    && cat /redis_data.txt | redis-cli --pipe \
    && redis-cli save \
    && redis-cli shutdown \
	&& redis-server

