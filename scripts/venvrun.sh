#!/bin/bash

cleanup() {
    while popd &>/dev/null; do dirs; done
}
trap cleanup EXIT

python="python3"
if [[ -n "${USEPYTHON}" ]]; then
    python="${USEPYTHON}"
fi

if [[ $(basename "${SHELL}") != "bash" ]]; then
    echo "I need bash" 1>&2
    exit 1
fi
basedir=$(readlink -f $(dirname $(readlink -f "${BASH_SOURCE[0]}"))/..)
me=$(basename "${basedir}")
myvenv="${basedir}/.venv"

[[ ! -d "${myvenv}" ]] && {
    "${python}" -m venv "${myvenv}"
    source "${myvenv}"/bin/activate
    pip install -U pip
    pip install uv
    pushd "${basedir}"
    uv sync
    ln -s basedpyright-langserver "${myvenv}"/bin/pyright-langserver
    popd
    deactivate
}
source "${myvenv}"/bin/activate
[[ "${#}" -gt 0 ]] && exec "${@}"
exec bash --noprofile --norc
