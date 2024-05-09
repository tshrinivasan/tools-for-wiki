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

export PYTHONUSERBASE="${basedir}/.python"
export MYVENV="${PYTHONUSERBASE}/${me}-venv"
export PIP_CACHE_DIR="${PYTHONUSERBASE}/pipcache"
export PYTHONPATH="${basedir}${PYTHONPATH:+:${PYTHONPATH}}"
export PATH="${PYTHONUSERBASE}/bin:${PATH}"
[[ ! -d "${MYVENV}" ]] && {
    mkdir -p "${PYTHONUSERBASE}"
    "${python}" -m venv "${MYVENV}"
    source "${MYVENV}"/bin/activate
    pushd "${basedir}"
    pip install .
    popd
    deactivate
}
source "${MYVENV}"/bin/activate
[[ "${#}" -gt 0 ]] && exec "${@}"
exec bash --noprofile --norc
