import httpx
from src.settings import get_settings

settings = get_settings()


async def verfiy_email_request(email: str):
    response = await httpx.AsyncClient().get(
        f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.EMAILHUNTER_API_KEY}"
    )
    print(response.json())
    return response.json()["data"]["status"] == "valid"
