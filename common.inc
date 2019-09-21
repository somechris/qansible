set -e
set -o pipefail

#---------------------------------------------------------------------
if [ -z "$ORIG_DIR_ABS" ]
then
    # First inclusion of common.inc
    ORIG_DIR_ABS="${PWD}"
fi

cd "$(dirname "$BASH_SOURCE[0]")"

if [ -z "$SCRIPT_DIR_ABS" ]
then
    # First inclusion of common.inc
    SCRIPT_DIR_ABS="${PWD}"
    SCRIPT_ARGUMENTS=( "$@" )
fi

SCRIPT_ROOT_DIR_ABS="${PWD}"

#---------------------------------------------------------------------

VIRTUAL_ENV_BIN_DIR_ABS="$HOME/.virtualenv/ansible/bin"

ANSIBLE_VERSION_MINIMUM=2.0.1
ANSIBLE_VERSION_TOO_HIGH=2.1.0

WARNINGS=0
VERBOSITY=0

LDAP_USER_NAME="$USER"  # You can use common.inc.local to override this.
LDAP_SSH_KEY_FILE="$HOME/.ssh/id_rsa"  # You can use common.inc.local to override this.

#---------------------------------------------------------------------
error() {
    echo "Error:" "$@" >&2
    exit 1
}

#---------------------------------------------------------------------
warn() {
	WARNINGS="$((WARNINGS+1))"
    echo "Warning:" "$@" >&2
}

#---------------------------------------------------------------------
blank_line() {
	echo
}

#---------------------------------------------------------------------
info() {
    if [ "$VERBOSITY" -ge 0 ]
    then
        echo "Info:" "$@"
    fi
}

#---------------------------------------------------------------------
verbose_info() {
    if [ "$VERBOSITY" -gt 0 ]
    then
	echo "Info: $@"
    fi
}

#---------------------------------------------------------------------
in_array() {
    local NEEDLE="$1"
    shift
    local HAY
    for HAY in "$@"
    do
        if [ "$HAY" = "$NEEDLE" ]
        then
            return 0
        fi
    done
    return 1
}

#---------------------------------------------------------------------
DEFAULT_OPTIONS_DOC="\
  --help                -- Shows this screen
  --quiet               -- Suppress purely informational messages
  --verbose, -v         -- Produces more verbose output
"

#---------------------------------------------------------------------
parse_default_option() {
    local ARGUMENT="$1"
    shift
    case "$ARGUMENT" in
        "--help" | "-h" | "-?" )
            print_help
            exit 1
            ;;
        "--verbose" | "-v" )
            VERBOSITY=$((VERBOSITY+1))
            ;;
        "--quiet" )
            VERBOSITY=-1
            ;;
        * )
            return 1
            ;;
    esac
}

#---------------------------------------------------------------------
assert_good_bash_command() {
    local BASH_COMMAND="/bin/bash"
    local BASH_MAJOR_VERSION="$("$BASH_COMMAND" --version | grep -i 'GNU bash, version [1-9]' | head -n 1 | sed -e 's/GNU bash, version \([1-9]*\)\..*$/\1/i')"
    local EXPECTED_BASH_MAJOR_VERSION=4

    if ! [ "$BASH_MAJOR_VERSION" -ge "$EXPECTED_BASH_MAJOR_VERSION" 2>/dev/null ]
    then
        # Either one of the two variables is not a number, or the
        # actual version is too low.
        if [ "$BASH_MAJOR_VERSION" -lt "$EXPECTED_BASH_MAJOR_VERSION" 2>/dev/null ]
        then
            error "Your '$BASH_COMMAND' points to bash in version $BASH_MAJOR_VERSION, while we're requiring at least $EXPECTED_BASH_MAJOR_VERSION. Please consult you OS how to upgrade. (If you are on MacOS, use homebrew)"
        else
            # Failed to arrive at a version number.
            error "Failed to detect version number to your '$BASH_COMMAND'. It reports as '$("BASH_COMMAND" --version 2>&1 || true)'. Either you're Bash looks incompatible, or you need to update the version check."
            echo fail bad
        fi
    fi
}
assert_good_bash_command

#---------------------------------------------------------------------
source "common_lint.inc"

#---------------------------------------------------------------------
set_inventory() {
    if [ -z "$ANSIBLE_INVENTORY" ]
    then
        local UPCOMING_ARG_IS_INVENTORY=
        while [ $# -gt 0 ]
        do
            if [ -n "$UPCOMING_ARG_IS_INVENTORY" ]
            then
                INVENTORY="$1"
                UPCOMING_ARG_IS_INVENTORY=
            fi
            local ARGUMENT="$1"
            shift || true
            case "$ARGUMENT" in
                "-i" | "--inventory" )
                    UPCOMING_ARG_IS_INVENTORY=yes
                    ;;
                * )
                    ;;
            esac
        done
    else
        INVENTORY="$ANSIBLE_INVENTORY"
    fi
}

#---------------------------------------------------------------------
set_inventory_link() {
    pushd "$SCRIPT_ROOT_DIR_ABS" >/dev/null
    local BASE="$1"
    local DEFAULT="$2"
    shift 2 || true

    local INVENTORY=
    set_inventory "$@"

    if [ -z "$INVENTORY" ]
    then
        # No inventory set on the command line. Hence, we try to parse
        # inventory from config file.
        INVENTORY=$(grep ^inventory.*= ansible.cfg | sed -e 's/^.*= *//' || true)

        if [ -z "$INVENTORY" ]
        then
            # Still no inventory found : -((
            error "No inventory given. Specify one using --inventory"
        fi
    fi

    if [ "$INVENTORY" != "${INVENTORY////}" ]
    then
        error "Since we're using the inventory name to automatically \
switch further parts of the setup, it must not contain slashes"
    fi

    local LINK_FILE="$BASE"
    local EXPECTED_TARGET="$BASE-$INVENTORY"

    if [ ! -e "$EXPECTED_TARGET" ]
    then
        if [ -n "$DEFAULT" ]
        then
            EXPECTED_TARGET="$DEFAULT"
        else
            error "target $EXPECTED_TARGET does not exist"
        fi
    fi

    local PRIVATE_TARGET="$(readlink "$LINK_FILE")" || true
    if [ -e "$LINK_FILE" -a -z "$PRIVATE_TARGET" ]
    then
        error "It seems '$LINK_FILE' is not a symbolic link, although it \
should be. Aborting"
    fi
    if [ -n "$PRIVATE_TARGET" -a "$PRIVATE_TARGET" != "$EXPECTED_TARGET" ]
    then
        rm "$LINK_FILE"
    fi
    if [ ! -e "$LINK_FILE" ]
    then
        ln -s "$EXPECTED_TARGET" "$LINK_FILE"
    fi
    popd >/dev/null
}

#---------------------------------------------------------------------
update_ssh_config() {
    pushd "$SCRIPT_ROOT_DIR_ABS" >/dev/null
    if [ -e "ssh/config.template" -a \( \
        ! -e "ssh/config" -o \
        "ssh/config" -ot "ssh/config.template" -o \
        \( -e "common.inc.local" -a "ssh/config" -ot "common.inc.local" \) \
        \) ]
    then
        sed \
            -e 's@\${LDAP_USER_NAME}@'"$LDAP_USER_NAME"'@g' \
            -e 's@\${LDAP_SSH_KEY_FILE}@'"$LDAP_SSH_KEY_FILE"'@g' \
            ssh/config.template > ssh/config
        # To ease using the config in ssh's Include command, we revoke
        # group and other permissions.
        chmod go-rwx ssh/config
    fi
    popd >/dev/null
}

#---------------------------------------------------------------------
set_inventory_links() {
    set_inventory_link private "" "$@"
    set_inventory_link ssh "$HOME/.ssh" "$@"
    update_ssh_config
}

#---------------------------------------------------------------------
assert_good_ansible_command() {
    local COMMAND="$1"
    local ANSIBLE_VERSION=$("$COMMAND" --version | head -n 1 | cut -f 2 -d ' ')

    if ! python - <<EOF
import sys
import distutils.version

MINIMUM = distutils.version.LooseVersion("$ANSIBLE_VERSION_MINIMUM")
TOO_HIGH = distutils.version.LooseVersion("$ANSIBLE_VERSION_TOO_HIGH")
ACTUAL = distutils.version.LooseVersion("$ANSIBLE_VERSION")

ret = MINIMUM <= ACTUAL
ret &= ACTUAL < TOO_HIGH

sys.exit(0 if ret else 1)
EOF
    then
        error "Incompatible Ansible version $ANSIBLE_VERSION. (Requiring at least $ANSIBLE_VERSION_MINIMUM, but below $ANSIBLE_VERSION_TOO_HIGH)"
    fi
}

#---------------------------------------------------------------------
run_ansible() {
    COMMAND="$1"
    shift || true
    if [ -d "$VIRTUAL_ENV_BIN_DIR_ABS" ]
    then
        COMMAND="$VIRTUAL_ENV_BIN_DIR_ABS/$COMMAND"
    fi

    assert_good_ansible_command "$COMMAND"

    if [ -n "$DEBUG_ANSIBLE_SHIM" ]
    then
        echo "$COMMAND" "$@"
        time "$COMMAND" "$@"
    else
        "$COMMAND" "$@"
    fi
}

#---------------------------------------------------------------------
run() {
	verbose_info "Running:" "$@"
	"$@"
}

#---------------------------------------------------------------------
confirm() {
    local QUESTION="$1"
    read -rp "$QUESTION (y/N) " ANSWER
    if [ "$ANSWER" != "y" ]
    then
        error "Answer is not 'y'. Aborting"
    fi
}

#---------------------------------------------------------------------

# Finally, include local overrides
if [ -f "${SCRIPT_ROOT_DIR_ABS}/common.inc.local" ]
then
    source "${SCRIPT_ROOT_DIR_ABS}/common.inc.local"
fi
