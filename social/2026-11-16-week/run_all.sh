#!/bin/bash
export PYTHONUTF8=1
cd "$(dirname "$0")"
run(){ for x in "$@"; do python render_week.py $x > "_log-$x.txt" 2>&1; done; }
run mon-16-studs mon-16-centauri tue-17-gifts tue-17-earring feed &
run wed-18-eternity wed-18-returning thu-19-zodiac &
run thu-19-algol fri-20-pendant fri-20-halo &
run sat-21-review sun-22-bf sun-22-all &
wait
echo ALLDONE
