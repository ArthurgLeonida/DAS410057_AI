#!/bin/sh

script_dir="$(CDPATH= cd "$(dirname "$0")" && pwd)"
optic_args=""
if [ "${OPTIMIZE:-0}" != "1" ]; then
  optic_args="-N"
fi
exit_code=0

for p in problem1 problem2 problem3 problem4; do
  echo
  echo "=== $p ==="
  docker run --rm \
    --entrypoint /root/planners/optic-clp \
    -v "${script_dir}:/x" \
    azathoth/pddl \
    $optic_args \
    /x/domain.pddl /x/$p.pddl || exit_code=$?
done

exit "$exit_code"
