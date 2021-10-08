
# Run project
1. copy _.env.example_ file in _.env_ file
2. Fill up with right credentials and variables inside.
3. run command **`docker-compose up --build`** 
4. during first run could occur error related to difference in creating containers for psql and django. 
It happens when django migrations run before database created. To solve it **Ctrl+C** and restart project.
the problem could be solved with **[healthcheck](https://stackoverflow.com/questions/35069027/docker-wait-for-postgresql-to-be-running)** docker-compose parameter.
5. Path to celery tasks _[/pricefetch/pricefetch/tasks.py](/home/user/PycharmProjects/pricefetch/pricefetch/tasks.py)_
