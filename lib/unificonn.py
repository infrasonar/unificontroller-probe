import aiohttp
import logging
import os
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from lib.asset_cache import AssetCache


async def login(asset: Asset, address: str, port: int, ssl: bool,
                username: str, password: str) -> dict:
    logging.debug(f'login on asset {asset}')

    auth_data = {
        'username': username,
        'password': password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'https://{address}:{port}/api/login',
            json=auth_data,
            ssl=ssl,
        ) as resp:
            if resp.status // 100 == 2:
                return {
                    'base_url': f'https://{address}:{port}',
                    'cookies': resp.cookies,
                }
            else:
                raise CheckException('login failed')


async def get_session(asset: Asset, asset_config: dict,
                      check_config: dict) -> dict:

    address = check_config.get('address')
    if not address:
        address = asset.name
    port = check_config.get('port', 443)
    ssl = check_config.get('ssl', False)
    username = asset_config.get('username')
    password = asset_config.get('password')

    # we use everything what identifies a connection for an asset as key
    # of the cached 'connection'
    connection_args = (address, port, ssl, username, password)
    session = AssetCache.get_value(connection_args)
    if session:
        return session

    try:
        session = await login(asset, *connection_args)
    except ConnectionError:
        raise CheckException('unable to connect')
    except Exception:
        raise
    else:
        # when connection is older than 3600 we request new 'connection'
        max_age = 3600
        AssetCache.set_value(connection_args, session, max_age)
    return session
