#!/usr/bin/env zsh

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

