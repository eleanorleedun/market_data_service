import uvicorn

from market_data_service.app import create_app
from market_data_service.config import get_settings


def main() -> None:
    settings = get_settings()

    uvicorn.run(
        create_app(),
        host=settings.host,
        port=settings.port,
    )


if __name__ == "__main__":
    main()
