# Juggler

This python script defines a "matrix test runner", which is basically a fancy way of saying ...

* Define one or more `docker-compose` templates
* Define a set of variables
* Combine compose templates and variables and run all combinations.

The idea is that you have a program / service / thing, which has to be integration tested, user acceptance tested, or otherwise tested, and you want to do this in an automated way using docker-compose environments.

For an example of a possible configuration see below.


## How this works

For most products you want to test them embedded in a system of connected components. For example if you use a database, it might be good to know with which versions of the database your product works, or that your latest build has still the same API functionality than your stable branch.

`intmaniac` enables you to write a parameterized `docker-compose`` template which describes your full test environment, and then run tests against it.

It is assumed that one container in your composition contains a test tool of the system, which is then executed with one or more commands. For this the testing container (the default name is `test-service`) is executed by intmania with a set of user-defined commands. `docker-compose` should bring up all dependent services on the first execution of the `docker-compose run` command.

*NOTE:* The tests are executed on the same host, all in parallel. You should have enough resources to ensure successful execution :) . If not, you can layer the test set defintions in an array, where all test sets in the outer array are executed sequentially. (see example at the bottom)

## Configuration examples


### intmaniac.yaml

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

      database-psql:        # a test set, contains tests

        postgres95:         # this is a test
          environment:
            DB_CONTAINER: postgres:9.5

        postgres94:         # and another
          environment:
            DB_CONTAINER: postgres:9.4

      database-maria:       # another test set

        maria10:            # with another test
          environment:
            DB_CONTAINER: maria:v10.0
            DB_PORT: 1111
            DB_TYPE: mysql
          meta:
            allow_failure: true

      configurations:   # aand another test set

        latest:
          environment:
            CONFIG_CONTAINER: my_config:latest


### docker-compose.yml

    # test-service is the default name. if you change it, you have
    # to set the meta.test_service key accordingly.
    test-service:

      image: my_company_hub/tests/runner

      # this is necessary to force docker-compose to create and start
      # the other services when starting test-service
      links:
        - test-me:test-me

    test-me:
      image: my_company_hub/%%TEST_CONTAINER%%
      environment:
        - DB_TYPE=%%DB_TYPE%%
        - DB_HOST=db
        - DB_PORT=%%DB_PORT%%
      links:
        - db:db

    db:
      image: my_company_hub/%%DB_CONTAINER%%


### intmaniac.yaml - sequential execution

If you want sequential execution of test(sets), then you can define multiple test set groups in an array. The test sets in this array are executed sequentially, and if the first set fails the second set is not executed.

    version: 1.0
    global: {}
    testsets:
      - testset1:
          testone:
            environment: {}
          testtwo:
            environment: {}
        testset2:
          testthree:
            environment: {}
      - testset3:
          testfour:
            environment: {}
