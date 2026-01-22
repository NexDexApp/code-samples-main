import asyncio
import logging
import os
import traceback

import aiohttp
from shared.api_client import get_nexdex_config
from onboarding import get_jwt_token, get_open_orders, perform_onboarding
from utils_hd import generate_nexdex_account_from_ledger

nexdex_http_url = "https://api.testnet.nexdex.trade/v1"


async def main(eth_account_address: str) -> None:
    # Load nexdex config
    nexdex_config = await get_nexdex_config(nexdex_http_url)

    # Generate nexdex account (from ledger)
    nexdex_account_address, nexdex_account_private_key_hex = generate_nexdex_account_from_ledger(
        nexdex_config, eth_account_address
    )

    # Onboard generated nexdex account
    logging.info("Onboarding...")
    await perform_onboarding(
        nexdex_config,
        nexdex_http_url,
        nexdex_account_address,
        nexdex_account_private_key_hex,
        eth_account_address,
    )

    # Get a JWT token to interact with private endpoints
    logging.info("Getting JWT...")
    nexdex_jwt = await get_jwt_token(
        nexdex_config,
        nexdex_http_url,
        nexdex_account_address,
        nexdex_account_private_key_hex,
    )

    # Get account's open orders using the JWT token
    logging.info("Getting account's open orders...")
    open_orders = await get_open_orders(nexdex_http_url, nexdex_jwt)

    print(f"Open Orders: {open_orders}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO"),
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        
    )

    # Load environment variables
    eth_account_address = os.getenv('ETHEREUM_ADDRESS', "")

    # Run main
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(eth_account_address))
    except Exception as e:
        logging.error("Local Main Error")
        logging.error(e)
        traceback.print_exc()
