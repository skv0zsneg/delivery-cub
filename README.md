# DELIVERY CUB

Simple Web-Application of Food Delivery Market "DELIVERY CUB"

## How to run

In your Linux terminal with all needed deps run:

For prod version

```bash
$ ./build.prod.sh
$ docker exec -it -u 0 delivery-cub-web-1 python manage.py collectstatic --no-input
```

If superuser isn't exist than go in running docker and execute^

```bash
$ docker-compose exec web python manage.py migrate --noinput
```
