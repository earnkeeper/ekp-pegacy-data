from decouple import config

from services.sync_transactions_cls import SyncTransactions
from services.parse_transactions_cls import ParseTransactions
if __name__ == '__main__':

    contract_address = '0x66e4e493bab59250d46bfcf8ea73c02952655206'
    # Pegaxy Market
    SyncTransactions(
        contract_address=contract_address,
        max_trans_to_fetch=config("MAX_TRANS_TO_FETCH", default=0, cast=int)
    )
    
    # PGX token
    # sync_transactions('0xc1c93D475dc82Fe72DBC7074d55f5a734F8cEEAE', mongo_db)

    ParseTransactions(contract_address=contract_address)
