#
#
#     D  E  P  R  E  C  A  T  E  D    !  !  !  !
#
#     This is the first version, only here to be of archive use.
#     It should have worked, though. It looked pretty good.
#
#

#!/usr/bin/env bash

# Each docker-compose run needs to have the following:
# $MYSELF - the container created HERE
# $COMPANIONx - with "x" being a number, one companion container
# we read or extract this from the environment

# $INT_TEST_RESULT_DIR - the (absolute) path to the test results
# this is created by us

# each test runner will place a file called "tests_done" in the directory
# when done
# this is created by the test runner, we react on it


#
# TeamCity output message functions
#

# $1 - required the block name
# $2 - optional the block description
tc_open() {
  [ ! -z "$2" ] && TMP="description='$2'" || TMP=""
  echo "##teamcity[blockOpened name='$1' $TMP ]"
}

# $1 - required the block name
tc_close() {
  echo "##teamcity[blockClosed name='$1']"
}

# $1 - required the message string
tc_msg() {
  echo "##teamcity[message text='$1']"
}

# $1 - required test name
tc_test_open() {
  echo "##teamcity[testStarted name='$1']"
}

# $1 - required test name
# $2 - required test fail message
# $3 - optional test fail detailed message
tc_test_fail() {
  [ ! -z "$3" ] && TMP="details='$3'" || TMP=""
  echo "##teamcity[testFailed name='$1' message='$2' $TMP ]"
}

# $1 - required test name
tc_test_close() {
  echo "##teamcity[testFinished name='$1']"
}


#
# Initialization functions
#

init() {
  if [ ! -d "inttest" ] ; then
    tc_msg "No 'inttest' directory for integration tests found. Exiting."
    exit 0
  fi
  source tc_settings.sh
  source BUILD_SETTINGS
  cd inttest                    # everything is happening in inttest ...
}


init_global_vars() {
  DOCKER_RUN_CMD="sudo docker-compose up -d"
  DOCKER_KILL_CMD="sudo docker-compose kill"
  #DOCKER_RUN_CMD="../check_vars.sh"
  #DOCKER_KILL_CMD="echo Test killed: "
  NUM_COMPANION_SETS=$(env | grep -E '^INT_TEST_COMPANION_SET_' | wc -l)
}


#
# Test functions
#

test_init_script_vars() {
  TEST_ID_BASE="INTTEST-${GITREF}-${BUILD_NUMBER}"
  TEST_ID="${TEST_ID_BASE}-${RUN}"
  # this is a bash array. see here: http://tldp.org/LDP/abs/html/arrays.html
  COMPANION_SET=( $(env \
      | grep -E '^INT_TEST_COMPANION_SET_' \
      | sort \
      | sed -ne "${RUN}p" \
      | sed -re 's/^[^=]+=//g' \
      ) )
}


# export all the vars which might be needed in sub-shells or invoked
# commands
test_init_export_vars() {
  # extract and set COMPANIONx variables from environment - works
  i=0
  for COMPANION in ${COMPANION_SET[@]} ; do
    eval "export INT_TEST_COMPANION_${i}=\"${COMPANION}\""
    (( i = $i + 1 ))
  done
  export INT_TEST_WORK_DIR=$(realpath "$(pwd)/${TEST_ID}")
  export INT_TEST_MYSELF="$DOCKER_TEMP_NAME"
  export INT_TEST_TESTRUNNER
}


test_init_work_dir() {
  rm -rf "$INT_TEST_WORK_DIR" # just to be sure, and for testing.
  mkdir "$INT_TEST_WORK_DIR"
  env | grep -E '^INT_TEST_' | sort >> "$INT_TEST_WORK_DIR/TEST_SETTINGS"
}


test_prepare_docker_template() {
  local COMPOSEYML="$INT_TEST_WORK_DIR/docker-compose.yml"
  local REPLACECMD="sed -ri $COMPOSEYML"
  cp docker-compose.yml.tmpl "$COMPOSEYML"
  # I *don't* know why, but docker-compose does not use find the env
  # variables and sets empty strings. using string replacement we circumvene
  # the problem
  $REPLACECMD \
    -e "s&%%INT_TEST_WORK_DIR%%&$INT_TEST_WORK_DIR&g" \
    -e "s&%%INT_TEST_MYSELF%%&$INT_TEST_MYSELF&g" \
    -e "s&%%INT_TEST_TESTRUNNER%%&$INT_TEST_TESTRUNNER&g"
  # replace all INT_TEST_COMPANION_x items
  # TODO - use bash arrays here ... (and below, for that matter)
  i=0
  for COMPANION in ${COMPANION_SET[@]} ; do
    $REPLACECMD -e "s&%%INT_TEST_COMPANION_${i}%%&${COMPANION}&g"
    (( i = $i + 1 ))
  done
}


test_start() {
  cd "$INT_TEST_WORK_DIR"
  $DOCKER_RUN_CMD
  if [ ! "$?" = "0" ] ; then
    echo "execStartFailure" > "TEST_FAIL"
  else
    echo $(date +%s) > "TEST_START"
  fi
  cd ..
}


# $1 - optional time limit for how long to wait in seconds
test_wait_for_done() {
  TEST_START=$(cat TEST_START)
  if [ -f "TEST_FAIL" ] ; then
    return 1
  fi
  while [ ! -f "TEST_DONE" ] ; do
    sleep 1
    if [ ! -z "$INT_TEST_TIMEOUT" -a ! $INT_TEST_TIMEOUT = "0" ] ; then
      if (( $i < $(date +%s) - $TEST_START )) ; then
        echo "execTimeoutFailure" > "TEST_FAIL"
        return 2
      fi
    fi
  done
  return
}


# $1 - required test id name (for docker compose to kill)
test_kill() {
  #$DOCKER_KILL_CMD && TMP="OK" || TMP="FAILURE!"
  #tc_msg "Killing containers of '$1': $TMP"
  $DOCKER_RM_CMD && TMP="OK" || TMP="FAILURE!"
  tc_msg "Removing containers of '$1': $TMP"
}


# pwd must be the test work directory
evaluate_tests() {
  for test_dir in $(ls "$TEST_ID_BASE"* -d | sort) ; do
    cd $test_dir
    test_wait_for_done
    test_kill $test_dir
    tc_test_open "$test_dir"
    if [ -f "TEST_FAIL" ] ; then
      tc_test_fail "$test_dir" "$(cat TEST_FAIL)"
    fi
    if [ -f "TEST_REPORT" ] ; then
      tc_open "Test report"
      cat TEST_REPORT
      tc_close "Test report"
    else
      tc_msg "No TEST_REPORT file found."
    fi
    if [ -f "TEST_SETTINGS" ] ; then
      tc_open "Test environment settings"
      cat TEST_SETTINGS
      tc_close "Test environment settings"
    fi
    if [ -f "docker-compose.yml" ] ; then
      tc_open "docker-compose configuration"
      cat docker-compose.yml
      tc_close "docker-compose configuration"
    fi
    tc_test_close "$test_dir"
    cd ..
  done
}


#
# START
#

init
init_global_vars

# we are 1-based, so nothing happens if "wc -l" returns 0 above. which is as
for RUN in $(seq 1 $NUM_COMPANION_SETS) ; do

  tc_msg "Start integration test #${RUN}"

  test_init_script_vars
  test_init_export_vars
  test_init_work_dir
  test_prepare_docker_template
  test_start

done

evaluate_tests
