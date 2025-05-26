import httpx
import os

async def post_data(data):
    url = os.getenv('ENDPOINT_URL')
    async with httpx.AsyncClient() as client:
        print(f"Posting data to {url}")
        print(f"Data being posted: {data}")
        resp = await client.post(url, json=data)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            # If response is not JSON, return raw text or None
            return resp.text  # or return None
