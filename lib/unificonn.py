import aiohttp
import logging
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException
from lib.asset_cache import AssetCache


async def login(asset: Asset, asset_config: dict, check_config: dict) -> dict:
    logging.debug(f'login on asset {asset}')

    address = check_config.get('address')
    if not address:
        address = asset.name
    username = asset_config.get('username')
    password = asset_config.get('password')

    auth_data = {
        'username': username,
        'password': password,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'https://{address}:8443/api/login',
            json=auth_data,
            ssl=False,
        ) as resp:
            if resp.status // 100 == 2:
                return {
                    'base_url': f'https://{address}:8443',
                    'cookies': resp.cookies,
                }
            else:
                logging.warning(f'login failed on {asset}')
                raise IgnoreResultException


async def get_session(asset: Asset, asset_config: dict,
                      check_config: dict) -> dict:
    session, _ = AssetCache.get_value(asset)
    if session:
        return session

    try:
        session = await login(asset, asset_config, check_config)
    except ConnectionError:
        raise CheckException('unable to connect')
    except Exception:
        raise
    else:
        AssetCache.set_value(asset, session)
    return session
