from google.adk.models.lite_llm import LiteLlm
from .configs import LITELLM_API_BASE, LITELLM_API_KEY

GEMINI_2_5_FLASH_PREVIEW_04_17 = LiteLlm(
    model="openai/gemini/gemini-2.5-flash-preview-04-17",
    api_base=LITELLM_API_BASE,
    api_key=LITELLM_API_KEY
)
