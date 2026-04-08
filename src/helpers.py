import asyncio
import base64
import hashlib


async def async_encode_base64(to_encode: str, max_len) -> str:
    return await asyncio.to_thread(encode_base64, to_encode, max_len)

def encode_base64(to_encode:str, max_len: int) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(to_encode.encode()).digest()).decode()[:max_len]
