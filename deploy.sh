fission spec init
fission env create --spec --name wtc-list-var-remove-env --image nexus.sigame.com.br/fission-wacth-list-variable-income-remove:0.2.0-0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-var-remove-fn --env wtc-list-var-remove-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-var-remove-rt --method DELETE --url /watch_list/variable_income/remove --function wtc-list-var-remove-fn
