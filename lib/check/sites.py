import aiohttp
from libprobe.asset import Asset
from lib.unificonn import get_session
from typing import Any


def float_or_none(inp: Any):
    if isinstance(inp, (float, int)):
        return float(inp)
    return None


async def check_sites(
    asset: Asset,
    asset_config: dict,
    check_config: dict
) -> dict:
    ssl = check_config.get('ssl', False)
    session, is_unifi_os = await get_session(asset, asset_config, check_config)
    url = '/proxy/network/api/stat/sites' if is_unifi_os else '/api/stat/sites'
    async with aiohttp.ClientSession(**session) as session:
        async with session.get(url, ssl=ssl) as resp:
            resp.raise_for_status()
            data = await resp.json()

    sites = [{
        'name': d['name'],  # str
        'desc': d.get('desc', d['name']),  # str
        'device_count': d['device_count'],  # int
        'location_accuracy': float_or_none(d.get('location_accuracy')),
        'location_lat': float_or_none(d.get('location_lat')),
        'location_lng': float_or_none(d.get('location_lng')),
    } for d in data['data']]

    return {
        'sites': sites
    }
