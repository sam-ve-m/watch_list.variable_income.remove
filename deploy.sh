fission spec init
fission env create --spec --name wtc-list-remove-env --image nexus.sigame.com.br/fission-wacth-list-remove:0.2.0-0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-remove-fn --env wtc-list-remove-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-remove-rt --method DELETE --url /watch_list/variable_income/remove --function wtc-list-remove-fn
