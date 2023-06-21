import logging

from src.scrapers.schemas.base import ParsedDatasetModel, ScrapeResultModel
from src.storage.data_access.base import BaseRepository
from src.storage.data_access.sqlite import SqliteRepository
from pprint import pprint

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(funcName)s | %(levelname)s: %(message)s",
    level=logging.INFO,
)

ALLOWED_SCRAPE_TIMEDELTA_SECONDS = 60


class MatchMatcher:
    def __init__(self, database: BaseRepository = SqliteRepository()) -> None:
        self._logger = logging.getLogger(self.__class__.__qualname__)
        self._database = database

    def _validate_batches_timestamps(self, timestamps: list[dict[str, str]]) -> list[str]:
        sorted_datetimes = sorted(
            timestamps, key=lambda entry: entry["scrape_end_time"]
        )
        time_deltas = [
            (
                sorted_datetimes[i + 1]["scrape_end_time"]
                - sorted_datetimes[i]["scrape_end_time"],
                sorted_datetimes[i]["scrape_id"],
                sorted_datetimes[i + 1]["scrape_id"],
            )
            for i in range(len(sorted_datetimes) - 1)
        ]

        biggest_delta, id1, id2 = max(
            time_deltas, key=lambda timedelta_id: timedelta_id[0]
        )

        self._logger.info(f"Biggest time delta:  {biggest_delta}")
        self._logger.info(f"IDs with the biggest gap: {id1}, {id2}")

        if biggest_delta.total_seconds() > ALLOWED_SCRAPE_TIMEDELTA_SECONDS:
            self._logger.warning(
                f"Delta between scrapes is bigger than {ALLOWED_SCRAPE_TIMEDELTA_SECONDS} seconds, skipping."
            )
            return []
        return [entry["scrape_id"] for entry in timestamps]

    def filter_and_sort_newest_batches(self) -> list[ParsedDatasetModel]:
        data = self._database.get_most_recent_bulks()
        scrape_id_timestamp = [
            {
                "scrape_id": model.scrape_id,
                "scrape_end_time": model.scrape_end_timestamp,
            }
            for model in data
        ]
        ids_to_use = self._validate_batches_timestamps(scrape_id_timestamp)

        return sorted(
            filter(lambda d: d.scrape_id in ids_to_use, data), key=lambda x: len(x.data)
        )

    def _find_match(self, match: ScrapeResultModel, matches: list[ParsedDatasetModel]):
        print(match)

        print(matches)

    def match_entities(self):
        packed_data = self.filter_and_sort_newest_batches()

        main, others = packed_data[0], packed_data[1:]

        results = []
        for entry in main.data:
            result = self._find_match(entry, others)
            print(result)
            break



if __name__ == "__main__":
    matcher = MatchMatcher()
    matcher.match_entities()