from abc import ABC, abstractmethod

from src.scrapers.schemas.base import ScrapeResultModelEnriched


class BaseRepository(ABC):
    @abstractmethod
    def insert_bulk(self, data: list[ScrapeResultModelEnriched]) -> None:
        pass

    @abstractmethod
    def get_most_recent_bulks(self) -> list[ScrapeResultModelEnriched]:
        pass

    @abstractmethod
    def delete_bulk(self) -> None:
        pass
