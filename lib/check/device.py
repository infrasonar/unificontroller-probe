import aiohttp
from libprobe.asset import Asset
from lib.unificonn import get_session


DEVICE_STATE = {
    0: 'offline',
    1: 'connected',
    2: 'pending adoption',
    4: 'updating',
    5: 'provisioning',
    6: 'unreachable',
    7: 'adopting',
    9: 'adoption error',
    10: 'adoption failed',
    11: 'isolated',
}


async def check_device(
    asset: Asset,
    asset_config: dict,
    check_config: dict
) -> dict:
    site_name = check_config.get('site', 'default')
    ssl = check_config.get('ssl', True)
    url = f'/api/s/{site_name}/stat/device-basic'
    session = await get_session(asset, asset_config, check_config)
    async with aiohttp.ClientSession(**session) as session:
        async with session.get(url, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    device = [{
        'name': d['name'],
        'mac': d.get('mac'),
        'state': DEVICE_STATE.get(d.get('state')),
        'adopted': d.get('adopted'),
        'disabled': d.get('disabled'),
        'type': d.get('type'),
        'model': d.get('model'),
        'in_gateway_mode': d.get('in_gateway_mode'),
    } for d in data['data']]

    return {
        'device': device
    }
