#!/bin/bash --init-file

## --- Config Variables ---
SHELL_RCFILES=${SHELL_RCFILES:-"/etc/bash.bashrc $HOME/.bashrc"}
VENV_NAME=${VENV_NAME:-venv}
VENV_PYTHON=${VENV_PYTHON:-python3}
VENV_FLAGS=${VENV_FLAGS:-"-q"}
PIP_FLAGS=${PIP_FLAGS:-"-q --no-python-version-warning"}

# Source shell rc files
for rcfile in $SHELL_RCFILES; do source $rcfile; done

function build_venv() {
    echo "Building virtualenv $VENV_NAME from scratch."
    
    # Create virtual environment
    $VENV_PYTHON -m venv $VENV_NAME $VENV_FLAGS
    
    # Activate the virtualenv
    source ./$VENV_NAME/bin/activate
    
    # Save the original deactivate function
    save_function deactivate venv_deactivate
    
    # Upgrade pip
    pip install --upgrade pip $PIP_FLAGS
    
    # Install requirements
    if [ -f "config/requirements.txt" ]; then
        pip install -r config/requirements.txt $PIP_FLAGS
    fi
}

function save_function() {
    local ORIG_FUNC=$(declare -f $1)
    local NEWNAME_FUNC="$2${ORIG_FUNC#$1}"
    eval "$NEWNAME_FUNC"
}

function rebuild_venv() {
    echo "Rebuilding virtual environment..."
    venv_deactivate
    rm -rf $VENV_NAME
    build_venv
}

if [ ! -d $VENV_NAME ]; then
    echo "Checking for ${BASH_SOURCE[0]} dependencies."
    DEPS_FOUND="yes"
    for dep in $VENV_PYTHON; do
        which $dep >/dev/null 2>/dev/null
        if [ $? -ne "0" ]; then
            echo Missing \"$dep\"
            DEPS_FOUND="no"
        fi
    done
    if [ "$DEPS_FOUND" == "no" ]; then
        echo "Found missing dependencies. Exiting."
        exit 1
    fi

    build_venv
fi

# Activate the virtualenv
source ./$VENV_NAME/bin/activate
save_function deactivate venv_deactivate

# Override the virtualenv deactivate with our function
function deactivate() {
    echo "Deactivating $VENV_NAME (i.e. exiting shell)."
    exit 0
}

function wshelp() {
    cat <<'END_OF_HELP' | sed 's/^    //'
    Commands:
      wshelp - This help message
      deactivate - Exits currently activated shell
      rebuild_venv - Deletes current venv and rebuilds it
END_OF_HELP
}

echo "Activation complete."
echo
echo "Type 'wshelp' to see available commands."
echo 