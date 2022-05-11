#!/usr/bin/env zsh

#Dev
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-uat-23be=tcp:12301
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1xpostgres-dev-23be=tcp:12302
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custodyuat-23be=tcp:12303
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custody-23be=tcp:12304
# atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-staging-23be=tcp:12305

/Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-uat-23be=tcp:12301,atoms-b1fs-dev-5320:asia-southeast1:ha-b1xpostgres-dev-23be=tcp:12302,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custodyuat-23be=tcp:12303,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-custody-23be=tcp:12304,atoms-b1fs-dev-5320:asia-southeast1:ha-b1x-staging-23be=tcp:12305

