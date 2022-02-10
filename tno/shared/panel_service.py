import json
import requests
from dataclasses import dataclass
from typing import Dict
from tno.shared.log import get_logger
from tno.flask_rest_api.settings import EnvSettings

logger = get_logger(__name__)


@dataclass
class PanelServiceResponse:
    _links: Dict
    dashboard_uid: str
    embed_url: str
    panel_id: int
    slug: str


def create_panel(data: Dict[str, any]) -> PanelServiceResponse:
    """Create a panel in the panel service.

    TODO: Create proper typing for the data variable.

    Args:
        data: The data to send to the panel service.

    Returns:
        PanelServiceResponse: The response from the panel service.
    """
    response = requests.post(
        f"http://{EnvSettings.panelservice_host()}:{EnvSettings.panelservice_port()}/graphs/",
        json=data,
        timeout=30,
    )
    logger.info(response)
    logger.info(response.content)
    try:
        parsed_response = json.loads(response.content)

        if "embed_url" in parsed_response:
            return PanelServiceResponse(**parsed_response)
        else:
            logger.error(parsed_response)
            raise Exception("Unexpected panel service response.")
    except Exception:
        logger.exception("Error parsing panel service response")
        raise
