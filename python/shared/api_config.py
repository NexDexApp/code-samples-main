"""
Description:
    nexdex client. To be replaced by generated stubs
"""
import ipaddress
import os

from .nexdex_api_utils import ApiConfigInterface


class ApiConfig(ApiConfigInterface):
    def __init__(self):
        self.nexdex_jwt = ""
        self.load_config()

    def load_config(self):
        """
        Load the configuration from env.
        """

        # nexdex Connection URLs

        self.nexdex_environment = os.getenv('nexdex_ENVIRONMENT', 'TESTNET')

        def local_to_testnet(env: str) -> str:
            if env == 'local':
                return 'testnet'
            return env

        self.nexdex_ws_url = (
            f'wss://ws.api.{local_to_testnet(self.nexdex_environment.lower())}.nexdex.trade/v1'
        )
        self.nexdex_http_url = (
            f'https://api.{local_to_testnet(self.nexdex_environment.lower())}.nexdex.trade/v1'
        )

        # Hex of the account contract address
        self.nexdex_account = os.getenv('nexdex_ACCOUNT', "")

        # Hex of the account private key (Stark Key)
        self.nexdex_account_private_key = os.getenv('nexdex_ACCOUNT_PRIVATE_KEY', "")

        self.ethereum_hd_phrase = os.getenv('ETHEREUM_HD_PHRASE', "")
        self.ethereum_account = os.getenv('ETHEREUM_ACCOUNT', "")
        self.ethereum_private_key = os.getenv('ETHEREUM_PRIVATE_KEY', "")
        self.quote_refresh_lower_boundary = float(os.getenv('QUOTE_REFRESH_LOWER_BOUNDARY', "0"))
        # Maximum time between attempts to submit orders
        self.quote_refresh_higher_boundary = float(
            os.getenv('QUOTE_REFRESH_HIGHER_BOUNDARY', "0.1")
        )

        self.ws_recv_timeout = int(os.getenv('WS_RECV_TIMEOUT', "1"))
        self.ws_heartbeat_period = int(os.getenv('WS_HB_PERIOD', "3"))
        self.needs_onboarding = False
        self.nexdex_config = dict()
        self.starknet_account = None
        self.pod_ip = os.getenv('POD_IP', '127.0.0.1')
        MAX_PODS = 15
        self.pod_index = int(ipaddress.IPv4Address(self.pod_ip)) % MAX_PODS
        return

    def __repr__(self):
        return str(vars(self))

    def to_dict(self) -> dict:
        config_dict = {}
        config_dict["nexdex_environment"] = self.nexdex_environment
        config_dict["nexdex_ws_url"] = self.nexdex_ws_url
        config_dict["nexdex_http_url"] = self.nexdex_http_url
        config_dict["nexdex_account"] = self.nexdex_account
        config_dict["nexdex_account_private_key"] = self.nexdex_account_private_key
        config_dict["ethereum_hd_phrase"] = self.ethereum_hd_phrase
        config_dict["ethereum_account"] = self.ethereum_account
        config_dict["ethereum_private_key"] = self.ethereum_private_key
        config_dict["quote_refresh_lower_boundary"] = self.quote_refresh_lower_boundary
        config_dict["quote_refresh_higher_boundary"] = self.quote_refresh_higher_boundary
        config_dict["ws_recv_timeout"] = self.ws_recv_timeout
        config_dict["ws_heartbeat_period"] = self.ws_heartbeat_period
        config_dict["needs_onboarding"] = self.needs_onboarding
        config_dict["pod_ip"] = self.pod_ip
        config_dict["pod_index"] = self.pod_index
        config_dict["nexdex_config"] = self.nexdex_config
        config_dict["starknet_account"] = self.starknet_account

        return config_dict
