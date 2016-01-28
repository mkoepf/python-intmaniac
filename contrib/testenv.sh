if [ "$1" = "" ] ; then
  echo "USAGE: $(basename $0) <2/3>"
  echo "And this script wants to be source'ed."
  false
elif ! $(python${1} --version > /dev/null 2>&1) ; then
  echo "ERROR: 'python${1}' exectuable not found"
  false
else
  env_name="intmaniac_install_test${1}"
  deactivate
  rmvirtualenv $env_name || true
  mkvirtualenv -p $(which python${i}) $env_name
fi
