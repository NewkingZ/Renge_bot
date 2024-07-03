import aiohttp
import asyncio
from asusrouter import AsusRouter, AsusData
from asusrouter.modules.led import AsusLED
from asusrouter.modules.parental_control import AsusParentalControl
import time

# Create a new event loop
loop = asyncio.get_event_loop()

# Create aiohttp session
session = None
router = None


async def connect_router():
    global session, router
    session = aiohttp.ClientSession()

    router = AsusRouter(
        hostname="192.168.50.1",
        username="Newking",
        password="udc!ie95yrAtzkf",
        use_ssl=True,
        session=session,
    )

    await router.async_connect()


async def get_system_info():
    res = await router.async_get_data(AsusData.RAM)
    print(res)
    time.sleep(2)
    res = await router.async_get_data(AsusData.CPU)
    print(res)
    time.sleep(2)


async def toggle_parent_controls(toggle):
    # Enables / Disables the
    res = await router.async_set_state(AsusParentalControl.ON if toggle else AsusParentalControl.OFF)
    print(res)