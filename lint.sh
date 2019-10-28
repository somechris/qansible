#!/bin/bash

LINT_HOST_VARS_WHITELISTED=() # host_vars files that do not need linting

source "$(dirname "$0")/common.inc"

MAIN_README_FILE_RELS="docs/README.txt"
LOCAL_ROLES_FILE_RELS=".local_roles"
TOX="$(which tox 2>/dev/null || true)"
VERBOSITY=0
REQUIRE_ALL=no

VAR_END_CHARS="a-zA-Z0-9"
VAR_CHARS="${VAR_END_CHARS}_"
VAR_BORDER_CHARS_LEFT="${VAR_CHARS}\"'"
VAR_BORDER_CHARS_RIGHT="${VAR_BORDER_CHARS_LEFT}("

SUB_LINTER_ARGUMENTS=()

#-----------------------------------------------------------------------
print_help() {
    cat <<EOF
lint.sh
=======

  lint.sh [ OPTIONS ]

Rudimentary linting of this repo. Returns 0, if all of the rudimentary
linting checks passed. Otherwise, returns != 0

OPTIONS:
$DEFAULT_LINTER_OPTIONS_DOC

  --require-all         -- Make all optional tests (e.g.: tox) required
EOF
}


#-----------------------------------------------------------------------
indent() {
    sed -e 's/^/   | /'
}


#-----------------------------------------------------------------------
parse_arguments() {
    while [ $# -gt 0 ]
    do
        local ARGUMENT="$1"
        shift
        case "$ARGUMENT" in
            "--require-all" )
                REQUIRE_ALL=yes
                ;;
            * )
                local SHIFT=0
                if parse_linter_default_option "$ARGUMENT" "$@"
                then
                    SUB_LINTER_ARGUMENTS+=("$ARGUMENT")
                    if [ "$SHIFT" != 0 ]
                    then
                        shift "$SHIFT"
                    fi
                else
                    error "Unknown argument '$ARGUMENT'"
                    print_help
                    exit 1
                fi
                ;;
        esac
    done
}


#-----------------------------------------------------------------------
echo_roles() {
    find roles -mindepth 1 -maxdepth 1 | cut -f 2 -d / | sort
}


#-----------------------------------------------------------------------
echo_non_local_roles() {
    echo_roles | while read ROLE
    do
        if ! in_array "$ROLE" "${LOCAL_ROLES[@]}"
        then
            echo "$ROLE"
        fi
    done
}


#-----------------------------------------------------------------------
run_sub_linters() {
    for SUB_LINTER in $(find -L -mindepth 2 -maxdepth 3 -type f -name 'lint*.sh' )
    do
        verbose_info "Sub-linter: $SUB_LINTER ..."

        local RUN="yes"
        if [ "$REQUIRE_ALL" != "yes" ]
        then
            verbose_info "Checking if linter $SUB_LINTER should run"
            if ! "$SUB_LINTER" --check-linter-requirements --quiet &>/dev/null
            then
                info "Skipping $SUB_LINTER, as requirements are not met"
                RUN="no"
            fi
        fi
        if [ "$RUN" = "yes" ]
        then
            verbose_info "Running sub-linter: $SUB_LINTER ..."
            if ! "$SUB_LINTER" "${SUB_LINTER_ARGUMENTS[@]}" | indent
            then
                warn "Sub-linter $SUB_LINTER failed"
                blank_line
            fi
        fi
    done
}

#-----------------------------------------------------------------------
lint_role() {
    local ROLE="$1"
    verbose_info "Role: $ROLE ..."

    local ROLE_VAR_START=${ROLE//-/_}

    if ! grep --quiet "^  - \`$ROLE\`: " "$MAIN_README_FILE_RELS"
    then
        warn "No description of role '$ROLE' in $MAIN_README_FILE_RELS"
    fi

    local ROLE_README_FILE_RELS="roles/$ROLE/README.txt"
    if [ -e "$ROLE_README_FILE_RELS" ]
    then
        if [ "$(head -n 1 "roles/$ROLE/README.txt")" != "Role: $ROLE" ]
        then
            warn "roles/$ROLE/README.txt does not start in 'Role: $ROLE'"
        fi

        local PATTERN
        for PATTERN in \
            "1. Description" \
            "2. Globals" \
            "3. Parameters" \

        do
            if [ "$(grep -c "^$PATTERN" "roles/$ROLE/README.txt")" != "2" ]
            then
                warn "Could not find two lines starting in $PATTERN in '$ROLE_README_FILE_RELS'"
            fi
        done

        # Check that all parameters of the role have documentation
        local VAR
        while IFS=: read FILE LINE_NO VAR REST
        do
            if ! grep --quiet '^\* `'"$VAR"'`: ' "roles/$ROLE/README.txt"
            then

                # We check if $VAR might belong to another
                # role. Because if we're in the role `foo`, and there
                # is also the role `foo-bar`, there is no need to warn
                # in role `foo` that documentation for `foo_bar_baz`
                # is missing.
                local BELONGS_TO_OTHER_ROLE=false
                local LAST_REMAINDER="${VAR}_helper"
                local REMAINDER="${VAR}"
                while [ "$BELONGS_TO_OTHER_ROLE" = "false" \
                    -a "$REMAINDER" != "$LAST_REMAINDER" \
                    -a -n "$REMAINDER" \
                    -a "${REMAINDER//_/-}" != "$ROLE" \
                    ]
                do
                    LAST_REMAINDER="$REMAINDER"
                    REMAINDER="${REMAINDER%_*}"
                    if [ -d "roles/${REMAINDER//_/-}" -a "${REMAINDER//_/-}" != "$ROLE" ]
                    then
                        # We found a role match, and it's not $ROLE itself. So
                        # we should ignore warning about this variable, here in
                        # $ROLE, as it belongs to the ${REMAINDER//_/-} role
                        # instead.
                        BELONGS_TO_OTHER_ROLE=true
                    fi
                done

                local LINT_IGNORE=false
                local FULL_LINE="$(sed -n "${LINE_NO}p" "$FILE" ; true)"
                if [ "lint-ignore" = "${FULL_LINE: -11}" \
                    -o "lint-ignore #}" = "${FULL_LINE: -14}" \
                    ]
                then
                    LINT_IGNORE=true
                fi

                if [ "$BELONGS_TO_OTHER_ROLE" = "false" -a "$LINT_IGNORE" = "false" ]
                then
                    if ! grep "^{# lint-ignore: $VAR " "$FILE" &>/dev/null
                    then
                        warn "Could not find documentation for variable '$VAR' (see $FILE, line $LINE_NO) in role '$ROLE'"
                    fi
                fi
            fi
        done < <(
            (
                # Direct role parameters
                for ASPECT in \
                    defaults \
                    vars \

                do
                    if [ -e "roles/$ROLE/$ASPECT/main.yml" ]
                    then
                        grep -Hn '^[a-zA-Z].*:' "roles/$ROLE/$ASPECT/main.yml"
                    fi
                done

                # Globals
                if [ -d "group_vars" ]
                then
                    grep -Rn "^${ROLE}_[a-zA-Z_-]*:" group_vars || true
                fi

                # Used variables throughout the checkout
                grep -HRnoP "(?<![$VAR_BORDER_CHARS_LEFT])${ROLE_VAR_START}_[$VAR_CHARS]*[$VAR_END_CHARS](?![$VAR_BORDER_CHARS_RIGHT])" roles group_vars host_vars 2>/dev/null \
                    | grep -v ":${ROLE_VAR_START}_\(reg\|fact\)_" \
                    || true
            ) \
                | ( grep '^[a-zA-Z]' || true ) \
                | sort -t : -k 3 -u
        )
        # Check that documented parameters are actually used.
        local VAR
        while IFS=: read FILE LINE_NO VAR REST
        do
            # The leading dot in the regexp helps to avoid matches
            # that define the variable in defaults/main.yml and
            # vars/main.yml. This is because in this check, we are not
            # interested in definitions of a variable, but usage of a
            # variable.
            if ! grep --quiet -HRnoP ".(?<![$VAR_BORDER_CHARS_LEFT])$VAR(?![$VAR_BORDER_CHARS_RIGHT])" \
                roles/*/defaults \
                roles/*/meta \
                roles/*/tasks \
                roles/*/templates \
                roles/*/vars \
                host_vars \
                group_vars \
                2>/dev/null
            then
                warn "$VAR (see $FILE line $LINE_NO) is unused. Please remove it."
            fi
        done < <( grep -Hn '^\* `[a-zA-Z0-9_]*`: ' "roles/$ROLE/README.txt" \
            | sed -e 's/\* `//' -e 's/`//' \
            || true )

    else
        warn "No README.txt for role '$ROLE'"
    fi

    if [ -d "roles/$ROLE/templates" ]
    then
        local TEMPLATE=
        for TEMPLATE in "roles/$ROLE/templates/"*
        do
            if [ -f "$TEMPLATE" ]
            then
                local TEMPLATE_FIRST_RELEVANT_LINE="$(grep -v '^\(#[!%]\|<?xml\)' "$TEMPLATE" | grep -v "^[[:space:]]*$" | head -n 1 || true)"
                if [[ ! "$TEMPLATE_FIRST_RELEVANT_LINE"  =~ "{{ansible_managed}}" ]]
                then
                    if [[ ! "$TEMPLATE_FIRST_RELEVANT_LINE"  =~ "{# qa:no-ansible-managed-check"(-#}|[, .#]) ]]
                    then
                      warn "Could not find {{ansible_managed}} marker in $TEMPLATE. Either add a '{{ansible_managed}} comment at the top of the file (after an eventual shebang), or add a '{# qa:no-ansible-managed-check, as <INSERT REASON HERE> -#}' Jinja comment."
                    fi
                fi
            fi
        done
    fi

    if [ -e "roles/$ROLE/meta/main.yml" ]
    then
        local FILE
        local LINE_NO
        local START
        local PADDED_ROLE
        local REST
        while IFS=: read FILE LINE_NO START PADDED_INCLUDED_ROLE REST
        do
            local INCLUDED_ROLE="$(sed -e 's/^[ 	]*//' -e 's/[ 	]*$//' <<<"$PADDED_INCLUDED_ROLE")"
            local INCLUDED_ROLE_MARKER="roles/$INCLUDED_ROLE/tasks/main.yml"
            if [ "${INCLUDED_ROLE}" = "${INCLUDED_ROLE%{{*}" ]
            then
                # '{{' does not occur in the role name, so there it's no template in the name
                if [ ! -f "$INCLUDED_ROLE_MARKER" ]
                then
                    # included role does not have tasks/main.yml file
                    warn "role '$ROLE' includes role '$INCLUDED_ROLE' in $FILE (line: $LINE_NO), but file '$INCLUDED_ROLE_MARKER' does not exist"
                fi
            fi
        done < <(  grep -HRnoP '^[         ]*-[    ]*role[  ]*:[   ]*(.*)[         ]*$' "roles/$ROLE/meta/main.yml" )
    fi
}


#-----------------------------------------------------------------------
lint_yaml() {
    local YAML_FILE_RELS="$1"

    # Guard against dense formatting of role inclusions
    while IFS=: read LINE_NUMBER LINE
    do
        warn "$YAML_FILE_RELS has a cruly brace followed by 'role:' in line $LINE_NUMBER ('$LINE'). Do not use one-line dicts for role definitions"
    done < <(grep -n '\{.*role:' "$YAML_FILE_RELS" || true)

    while IFS=: read FILE LINE_NO LINE
    do
        warn "$YAML_FILE_RELS has a '=' before a ':' in line $LINE_NO. This should probably be a ':'. The full line is: $LINE"
    done < <(grep -n '^[a-zA-Z0-9_" ]*[^!=]=[^=].*' "$YAML_FILE_RELS" )

    while IFS=: read FILE LINE_NO LINE
    do
        warn "$YAML_FILE_RELS has a top level item not starting in a name setting. Please add a name setting. The full line is: $LINE"
    done < <(grep -n '^- ' "$YAML_FILE_RELS" | grep -v '^[0-9]*:- \(name\|include\|import_playbook\):' )
}


#-----------------------------------------------------------------------
lint_roles() {
    local ROLE
    for ROLE in $(echo_non_local_roles)
    do
        lint_role "$ROLE"
    done
}

#-----------------------------------------------------------------------
lint_host_vars_file() {
    local HOST_VARS_FILE_RELS="$1"
    local HOST_VARS_FILE_RELH="${HOST_VARS_FILE_RELS:10}"
    if [ "${HOST_VARS_FILE_RELH: -9}" = "/main.yml" -o "${HOST_VARS_FILE_RELH////_}" = "${HOST_VARS_FILE_RELH}" ]
    then
        # The file is the main YAML file for a host
        if ! grep -q ^public_ipv4_address "$HOST_VARS_FILE_RELS"
        then
            if ! in_array "$HOST_VARS_FILE_RELH" "${LINT_HOST_VARS_WHITELISTED[@]}"
            then
                warn "$HOST_VARS_FILE_RELS does not have an IP address. Either grant the host an IP address, or drop the configs for it."
            fi
        fi
    fi
}


#-----------------------------------------------------------------------
lint_host_vars() {
    local HOST_VARS_FILE_RELS
    for HOST_VARS_FILE_RELS in $(find host_vars -type f)
    do
        lint_host_vars_file "$HOST_VARS_FILE_RELS"
    done
}


#-----------------------------------------------------------------------
lint_yamls() {
    local YAML_FILE_RELS
    for YAML_FILE_RELS in $(find -type f \( -iname '*.yaml' -o -iname '*.yml' \) )
    do
        lint_yaml "$YAML_FILE_RELS" >&2
    done

    for YAML_FILE_RELS in $(find host_vars -type f)
    do
        lint_yaml "$YAML_FILE_RELS" >&2
    done
}


#-----------------------------------------------------------------------
run_tox() {
    if [ -x "$TOX" ]
    then
        verbose_info "Starting tox ..."
        if tox >.tox-output 2>&1
        then
            if [ "$VERBOSITY" -gt 0 ]
            then
                cat .tox-output | indent
            fi
        else
            cat .tox-output | indent
            warn "tox failed"
        fi
        rm -f .tox-output
    else
        if [ "$REQUIRE_ALL" = "yes" ]
        then
            warn "Could not find tox. Please install it."
        else
            info "Skipping tox tests, as tox is not installed"
        fi
    fi
}


#-----------------------------------------------------------------------
if [ -e "$LOCAL_ROLES_FILE_RELS" ]
then
    readarray -t LOCAL_ROLES <"$LOCAL_ROLES_FILE_RELS"
else
    LOCAL_ROLES=()
fi

parse_arguments "$@"

lint_roles
lint_host_vars
lint_yamls

run_sub_linters

run_tox

finish_linting
