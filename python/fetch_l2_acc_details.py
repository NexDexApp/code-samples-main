import asyncio
import logging
import os
from typing import Dict, List
from shared.api_client import get_nexdex_config
from utils import (
    generate_nexdex_account,
    get_l1_eth_account,
)

nexdex_http_url = "https://api.testnet.nexdex.trade/v1"
async def main(eth_private_key_hex: str) -> None:
    # Initialize Ethereum account
    _, eth_account = get_l1_eth_account(eth_private_key_hex)

    # Load nexdex config
    nexdex_config = await get_nexdex_config(nexdex_http_url)

    # Generate nexdex account (only local)
    nexdex_account_address, nexdex_account_private_key_hex = generate_nexdex_account(
        nexdex_config, eth_account.key.hex()
    )
    print(f"nexdex Account Address: {nexdex_account_address}")
    print(f"nexdex Account Private Key: {nexdex_account_private_key_hex}")


if __name__ == "__main__":
    # Logging
    logging.basicConfig(
        level=os.getenv("LOGGING_LEVEL", "INFO"),
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Load environment variables
    eth_private_key_hex = os.getenv('ETHEREUM_PRIVATE_KEY', "")
    asyncio.run(main(eth_private_key_hex))
