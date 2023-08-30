import aiohttp
from libprobe.asset import Asset
from lib.unificonn import get_session


async def check_health(
    asset: Asset,
    asset_config: dict,
    check_config: dict
) -> dict:
    site_name = check_config.get('site', 'default')
    ssl = check_config.get('ssl', True)
    url = f'/api/s/{site_name}/stat/health'
    session = await get_session(asset, asset_config, check_config)
    async with aiohttp.ClientSession(**session) as session:
        async with session.get(url, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    health = [{
        'name': d['subsystem'],
        'num_user': d.get('num_user'),
        'num_guest': d.get('num_guest'),
        'num_iot': d.get('num_iot'),
        'tx_bytes_r': d.get('tx_bytes-r'),
        'rx_bytes_r': d.get('rx_bytes-r'),
        'status': d.get('status'),
        'num_ap': d.get('num_ap'),
        'num_adopted': d.get('num_adopted'),
        'num_disabled': d.get('num_disabled'),
        'num_disconnected': d.get('num_disconnected'),
        'num_pending': d.get('num_pending'),
    } for d in data['data']]

    return {
        'health': health
    }
