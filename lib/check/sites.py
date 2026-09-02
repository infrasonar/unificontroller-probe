import aiohttp
import logging
from libprobe.asset import Asset
from libprobe.check import Check
from lib.unificonn import get_credentials, sanity_check
from typing import Any
from ..connector import get_connector


def float_or_none(inp: Any):
    if isinstance(inp, (float, int)):
        return float(inp)
    return None


class CheckSites(Check):
    key = 'sites'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:
        ssl = config.get('ssl', False)
        credentials = await get_credentials(asset, local_config, config)

        base_url = credentials['base_url']
        is_unifi_os = credentials['is_unifi_os']
        cookies = credentials['cookies']
        headers = credentials['headers']

        prefix = '/proxy/network' if is_unifi_os else ''
        url = f"{base_url}{prefix}/api/self/sites"

        async with aiohttp.ClientSession(cookies=cookies,
                                         connector=get_connector()) as session:
            async with session.get(url, headers=headers, ssl=ssl) as resp:
                await sanity_check(resp, url)
                data = await resp.json()

        sites = [{
            'name': site['name'],
            'desc': site.get('desc', site['name']),
            'device_count': site.get('device_count', 0),
            'location_accuracy': float_or_none(site.get('location_accuracy')),
            'location_lat': float_or_none(site.get('location_lat')),
            'location_lng': float_or_none(site.get('location_lng')),
        } for site in data.get('data', [])]

        return {
            'sites': sites
        }
