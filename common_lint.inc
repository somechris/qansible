DEFAULT_LINTER_OPTIONS_DOC="\
$DEFAULT_OPTIONS_DOC\
  --check-linter-requirements
                        -- Check if the linter has all it's requirements met
                           and can run properly (but do not run linter yet).
"

#---------------------------------------------------------------------
parse_linter_default_option() {
    local ARGUMENT="$1"
    shift
    case "$ARGUMENT" in
        "--check-linter-requirements")
            check_linter_requirements
            exit 0
            ;;
        * )
            if parse_default_option  "$ARGUMENT" "$@"
            then
                return 0
            fi
            return 1
            ;;
    esac
}

#---------------------------------------------------------------------
check_linter_requirements() {
    :
}


#---------------------------------------------------------------------
finish_linting() {
    local DESCRIPTION="$1"
    if [ -n "$DESCRIPTION" ]
    then
        DESCRIPTION=" $DESCRIPTION"
    fi

    if [ "$WARNINGS" != "0" ]
    then
        error "Linting$DESCRIPTION failed due to $WARNINGS warnings"
    fi
    verbose_info "Linting$DESCRIPTION passed"
}
