#!/bin/bash

#set -x
export PS4='+ [`basename ${BASH_SOURCE[0]}`:$LINENO ${FUNCNAME[0]} \D{%F %T} $$ ] '
CURDIR=$(cd "$(dirname "$0")"; pwd);
MYNAME="${0##*/}"

g_INDEX_FILE="indexlist"
g_CLUSTERIP="127.0.0.1"
g_DELETE=0
g_LIST=0
g_NUM=1

RET_OK=0
RET_FAIL=1

##################### function #########################
_report_err() { echo "${MYNAME}: Error: $*" >&2 ; }

if [ -t 1 ]
then
    RED="$( echo -e "\e[31m" )"
    HL_RED="$( echo -e "\e[31;1m" )"
    HL_BLUE="$( echo -e "\e[34;1m" )"

    NORMAL="$( echo -e "\e[0m" )"
fi

_hl_red()    { echo "$HL_RED""$@""$NORMAL";}
_hl_blue()   { echo "$HL_BLUE""$@""$NORMAL";}

_trace() {
    echo $(_hl_blue '  ->') "$@" >&2
}

_print_fatal() {
    echo $(_hl_red '==>') "$@" >&2
}

_is_number() {
    local re='^[0-9]+$'
    local number="$1"

    if [ "x$number" == "x" ]; then
        _print_fatal "error: _is_number need one parameter"
        exit 1
    else
        number=${number//[[:space:]]/}
    fi

    if ! [[ $number =~ $re ]] ; then
        _print_fatal "error: ${number} not a number" >&2
        exit 1
    else
        return 0
    fi
}

_usage() {
    cat << USAGE
Usage: bash ${MYNAME} [options].

Options:
    -n, --number     num   Nummber for delete oldest index, default: 1.
    -c, --clusterip  ip    IP for elasticsearch cluster, default: 127.0.0.1.
    -d, --delete           If delete the index, default:0.
    -l, --list             List all index for display.
    -h, --help             Print this help infomation.

USAGE

    exit 1
}

#
# Parses command-line options.
#  usage: _parse_options "$@" || exit $?
#
_parse_options()
{
    declare -a argv

    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--delete)
                g_DELETE=1
                shift
                ;;
            -l|--list)
                g_LIST=1
                shift
                ;;
            -c|--clusterip)
                g_CLUSTERIP=${2}
                shift 2
                ;;
            -n|--number)
                g_NUM=${2}
                _is_number "${g_NUM}"
                shift 2
                ;;
            -h|--help)
                _usage
                exit
                ;;
            --)
                shift
                argv=("${argv[@]}" "${@}")
                break
                ;;
            -*)
                _print_fatal "command line: unrecognized option $1" >&2
                return 1
                ;;
            *)
                argv=("${argv[@]}" "${1}")
                shift
                ;;
        esac
    done
}

_parse_options "${@}" || _usage

if [ "x${g_LIST}" = "x1" ]; then
    ## list all index by order.
    _trace "List all index on the cluster: $g_CLUSTERIP..............."
    curl -s "${g_CLUSTERIP}:9200/_cat/indices?v" | awk '{print $3}' | grep -vP "index|kibana|marvel" | sort
    exit 0
else
    ## list all index by order.
    curl -s "${g_CLUSTERIP}:9200/_cat/indices?v" | awk '{print $3}' | grep -vP "index|kibana|marvel" | sort | head -"${g_NUM}" &> "$g_INDEX_FILE"
fi

## batch manage index.
if [ "x${g_DELETE}" = "x0" ]; then
    echo "The $g_NUM oldest index list is:"
fi

while read -r index
do
    if [ "x${g_DELETE}" = "x1" ]; then
        _trace "deleting index: $index ......"
        curl -XDELETE "${g_CLUSTERIP}:9200/$index?pretty"
    else
        _trace "$index"
    fi
done < "$g_INDEX_FILE"

if [ -e ${g_INDEX_FILE} ]; then rm -rf $g_INDEX_FILE; fi