import aiohttp
import logging
import os
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from lib.connection_cache import ConnectionCache


async def login(asset: Asset, address: str, port: int, ssl: bool,
                username: str, password: str) -> dict:
    logging.debug(f'login on asset {asset}')

    auth_data = {
        'username': username,
        'password': password,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://{address}:{port}/api/auth/login',
                json=auth_data,
                ssl=ssl,
            ) as resp:
                resp.raise_for_status()
                return {
                    'base_url': f'https://{address}:{port}',
                    'cookies': resp.cookies,
                }
    except Exception as e:
        msg = str(e) or type(e).__name__
        raise CheckException(f'login failed: {msg}')


async def get_session(asset: Asset, asset_config: dict,
                      check_config: dict) -> dict:

    address = check_config.get('address')
    if not address:
        address = asset.name
    port = check_config.get('port', 443)
    ssl = check_config.get('ssl', False)
    username = asset_config.get('username')
    password = asset_config.get('password')
    if None in (username, password):
        raise CheckException('missing credentials')

    # we use everything what identifies a connection for an asset as key
    # of the cached 'connection'
    connection_args = (address, port, ssl, username, password)
    session = ConnectionCache.get_value(connection_args)
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
        ConnectionCache.set_value(connection_args, session, max_age)
    return session
