# toucan_toco_test_project_server

## Project setup
You'll need to do it each time you add a new requirements
```shell script
cd deploy-dev
docker-compose build
```

### Development run
```shell script
cd deploy-dev
docker-compose up
```

### Launch tests
```shell script
cd deploy-dev
docker-compose run toucan_toco_test_project_server python -m pytest
```
You can use `docker-compose exec` instead if you container is already running.