#!/bin/bash

source "$(dirname "$0")/common.inc"

set_inventory_links "$@"

run_ansible $(basename "$0" ".sh") "${COMMON_OPTIONS[@]}" "$@"
