from dataclasses import dataclass

from src.enums import Bookmaker
from src.scrapers.schemas.base import ScrapeResultModelEnriched, ScrapeResultModel


BookmakersDatasets = dict[Bookmaker, list[ScrapeResultModelEnriched]]


@dataclass
class EntityMatcherModel:
    bookmaker: Bookmaker
    match_data: ScrapeResultModel
