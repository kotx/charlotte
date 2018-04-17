# Source: https://github.com/slice/dogbot/blob/master/dog/haste.py



""" Facilities for pasting things to Hastebin. """



# noinspection PyPackageRequirements

import aiohttp



HASTEBIN_ENDPOINT = 'https://haste.torque.ink/documents'

HASTEBIN_FMT = 'https://haste.torque.ink/{}'





async def haste(session: aiohttp.ClientSession, text: str) -> str:
    """ Pastes something to Hastebin, and returns the link to it. """

    async with session.post(HASTEBIN_ENDPOINT, data=text) as resp:
        resp_json = await resp.json()
        return HASTEBIN_FMT.format(resp_json['key'])


