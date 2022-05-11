

import psycopg2

#the database connection to be used
user = "bfetterman@b1ops.net"
database = "b1x-ha-prod-cordis-transactions"
dbhost = "127.0.0.1"
dbport = "5432"
password = ""
try:
    conn = psycopg2.connect(f"dbname={database} user={user} host={dbhost} password={password} port={dbport}")
except Exception as e:
    print("{e.__class__} occurred.")
    raise
tradeAccountId = input('\nPlease input the trade account id\n')
assetSymbol = input('\nPlease input the asset symbol\n')
startTime = input('\nPlease input the start time (YYYY-MM-DD HH:MM:SS.sss)\n')
endTime = input('\nPlease input the end time (YYYY-MM-DD HH:MM:SS.sss)\n')
cur = conn.cursor()
cur.execute("SELECT sub.* FROM (SELECT to_char(sah.ds_created_at, 'YYYY-MM-DD HH:MM:SS.ssssss'), sah.available_quantity, sah.available_quantity - LAG(sah.available_quantity, 1)  OVER (ORDER BY ds_created_at) as diff, ac.symbol, sah.asset_id, sah.event_type FROM cordis.spot_account_history sah JOIN cordis.asset_config ac on ac.asset_id = sah.asset_id WHERE trading_account_id = %s AND ac.symbol= %s AND ds_created_at BETWEEN %s and %s ORDER BY ds_created_at) sub WHERE event_type !='64';", (tradeAccountId, assetSymbol, startTime, endTime))
results = cur.fetchall()
for r in results:
    print(r)
conn.close()
