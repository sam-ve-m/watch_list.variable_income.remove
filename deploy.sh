#!/bin/bash
fission spec init
fission env create --spec --name watch-list-remove-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name watch-list-remove-fn --env watch-list-remove-env --src "./func/*" --entrypoint main.remove_symbols  --rpp 100000
fission route create --spec --method DELETE --url /watch_list/remove --function watch-list-remove-fn
