# Juggler

This python script defines a "matrix test runner", which is basically a fancy way of saying ...

* Define one or more `docker-compose` templates
* Define a set of variables
* Combine compose templates and variables and run all combinations.

The idea is that you have a program / service / thing, which has to be integration tested, user acceptance tested, or otherwise tested, and you want to do this in an automated way using docker-compose environments.

For an example of a possible configuration see below.


## Configuration examples


### juggler.yaml

    ---
    version: 1.0            # no effect so far
    global:
      environment:
        TEST_CONTAINER: my_container:v1.0
        CONFIG_CONTAINER: my_config:v1.0
        DB_CONTAINER: postgres:9.3
        DB_PORT: 5432
        DB_TYPE: postgres

    testsets:

      # this is a test group. the config settings under "global" above are
      # applied unless overwritten by the unique tests

      database-tests:

        # this is a test
        postgres95:      # this is a test
          environment:
            DB_CONTAINER: postgres:9.5

        postgres94:
          environment:
            DB_CONTAINER: postgres:9.4

        # another test group, with another test
        mariadb:

          maria10:
            environment:
              DB_CONTAINER: maria:v10.0
              DB_PORT: 1111
              DB_TYPE: mysql
            meta:
              allow_failure: true

        config-test:

          # This test will override the global CONFIG_CONTAINER setting
          # and will happen with postgres 9.3
          latest: { environment: { CONFIG_CONTAINER: my_config:latest } }


### docker-compose.yml

    test-me:
      image: %%TEST_CONTAINER%%
      environment:
        - DB_TYPE=%%DB_TYPE%%
        - DB_HOST=db
        - DB_PORT=%%DB_PORT%%
      links:
        - db:db
    db:
      image: %%DB_CONTAINER%%
