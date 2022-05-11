#!/usr/bin/env zsh

# kill -9 `ps ax |grep cloud_sql_proxy | grep -v grep | awk {'print$1'}`
killall cloud_sql_proxy

#PROD
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cordis-transactions-144d-replica1=tcp:12501 &
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-ctrl-144d-replica1=tcp:12502 &
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-custody-transactions-144d-replica1=tcp:12503 &
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-notifications-144d-replica1=tcp:12504 &
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-pii-144d-replica1=tcp:12505 &
# /Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cerebro-144d-replica1=tcp:12507 &


# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cordis-transactions-144d-replica1=tcp:12501
# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-ctrl-144d-replica1=tcp:12502
# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-custody-transactions-144d-replica1=tcp:12503
# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-notifications-144d-replica1=tcp:12504
# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-pii-144d-replica1=tcp:12505
# atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cerebro-144d-replica1=tcp:12507

/Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cordis-transactions-144d-replica1=tcp:12501,atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-ctrl-144d-replica1=tcp:12502,atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-custody-transactions-144d-replica1=tcp:12503,atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-notifications-144d-replica1=tcp:12504,atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-pii-144d-replica1=tcp:12505,atoms-b1fs-prod-7c40:asia-southeast1:b1x-ha-prod-cerebro-144d-replica1=tcp:12507 &


#Pub
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-bugbounty-1044=tcp:12401
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-simnext-1044=tcp:12402
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-internal-1044=tcp:12403

/Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-bugbounty-1044=tcp:12401,atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-simnext-1044=tcp:12402,atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-internal-1044=tcp:12403 &

#Dev
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-uat-23be=tcp:12301
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1xpostgres-dev-23be=tcp:12302
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custodyuat-23be=tcp:12303
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custody-23be=tcp:12304
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-staging-23be=tcp:12305

/Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-uat-23be=tcp:12301,atoms-b1fs-dev-5320:asia-southeast1:ha-b1xpostgres-dev-23be=tcp:12302,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custodyuat-23be=tcp:12303,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custody-23be=tcp:12304,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-staging-23be=tcp:12305

