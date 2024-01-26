import aiohttp
from libprobe.asset import Asset
from lib.unificonn import get_session
from urllib.parse import quote


async def check_alarms(
    asset: Asset,
    asset_config: dict,
    check_config: dict
) -> dict:
    site_name = check_config.get('site', 'default')
    ssl = check_config.get('ssl', False)
    session, is_unifi_os = await get_session(asset, asset_config, check_config)
    uri = '/proxy/network/api/s/' if is_unifi_os else '/api/s/'
    url = f'{uri}{quote(site_name, safe="")}/stat/alarm'
    async with aiohttp.ClientSession(**session) as session:
        async with session.get(url, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    # TODO find out what we need
    return {
        'alarms': data
    }
