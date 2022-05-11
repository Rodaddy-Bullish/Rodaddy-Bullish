# PROD
# b1x-ha-prod-cordis-transactions-144d-replica1=tcp:12501
# b1x-ha-prod-ctrl-144d-replica1=tcp:12502
# b1x-ha-prod-custody-transactions-144d-replica1=tcp:12503
# b1x-ha-prod-notifications-144d-replica1=tcp:12504
# b1x-ha-prod-pii-144d-replica1=tcp:12505
# b1x-ha-prod-cerebro-144d-replica1=tcp:12507

# PUB
# b1x-ha-bugbounty-1044=tcp:12401
# b1x-ha-simnext-1044=tcp:12402
# b1x-ha-internal-1044=tcp:12403

# DEV
# ha-b1x-uat-23be=tcp:12301
# ha-b1xpostgres-dev-23be=tcp:12302
# ha-b1x-custodyuat-23be=tcp:12303
# ha-b1x-custody-23be=tcp:12304
# ha-b1x-staging-23be=tcp:12305


USER = "bfetterman@b1ops.net"

db1x = {
    'prodCordis': dict(user=USER, password="", host="127.0.0.1", dbPort=12501),
    'prodCtrl': dict(user=USER, password="", host="127.0.0.1", dbPort=12502),
    'prodCustody': dict(user=USER, password="", host="127.0.0.1", dbPort=12503),
    'prodPii': dict(user=USER, password="", host="127.0.0.1", dbPort=12505),
    'prodCerebro': dict(user=USER, password="", host="127.0.0.1", dbPort=12507),
    'bugBounty': dict(user=USER, password="", host="127.0.0.1", dbPort=12401),
    'simNext': dict(user=USER, password="", host="127.0.0.1", dbPort=12402),
    'internal': dict(user=USER, password="", host="127.0.0.1", dbPort=12403),
    'uat': dict(user=USER, password="", host="127.0.0.1", dbPort=12301),
    'dev': dict(user=USER, password="", host="127.0.0.1", dbPort=12302),
    'custodyUat': dict(user=USER, password="", host="127.0.0.1", dbPort=12303),
    'custody': dict(user=USER, password="", host="127.0.0.1", dbPort=12304),
    'staging': dict(user=USER, password="", host="127.0.0.1", dbPort=12305)
}
