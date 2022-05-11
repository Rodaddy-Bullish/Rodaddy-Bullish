#!/usr/bin/env zsh

#Pub
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-bugbounty-1044=tcp:12401
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-simnext-1044=tcp:12402
# atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-internal-1044=tcp:12403

/Users/rico.rojas/Development/sql_proxy/cloud_sql_proxy -enable_iam_login -log_debug_stdout -instances=atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-bugbounty-1044=tcp:12401,atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-simnext-1044=tcp:12402,atoms-b1fs-pub-1be0:asia-southeast1:b1x-ha-internal-1044=tcp:12403 &

