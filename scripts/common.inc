if [ -z "$ORIG_DIR_ABS" ]
then
    # First inclusion of common.inc
    ORIG_DIR_ABS="${PWD}"
fi

cd "$(dirname "$BASH_SOURCE[0]")"
pushd . >/dev/null

if [ -z "$SCRIPT_DIR_ABS" ]
then
    # First inclusion of common.inc
    SCRIPT_DIR_ABS="${PWD}"
    SCRIPT_ARGUMENTS=( "$@" )
fi

SCRIPT_ROOT_DIR_ABS="${SCRIPT_ROOT_DIR_ABS:-$SCRIPT_DIR_ABS}"

#---------------------------------------------------------------------
# Not using ".." to avoid dereferencing of symbolic links.
SCRIPT_PARENT_DIR_ABS="${PWD%/*}"
if [ -e "$SCRIPT_PARENT_DIR_ABS/common.inc" ]
then
    source "$SCRIPT_PARENT_DIR_ABS/common.inc"
fi

#---------------------------------------------------------------------
popd >/dev/null
