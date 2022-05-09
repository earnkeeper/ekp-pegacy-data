from db.init_db import init_db
from sync_transactions import sync_transactions

init_db()

# Pegaxy Market
sync_transactions('0x66e4e493bab59250d46bfcf8ea73c02952655206')
# PGX token
sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE')

parse_transactions()
