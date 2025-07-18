from langops.parser.utils.resolver import PatternResolver
from langops.parser.utils.stage_cleaner import STAGE_NAME_CLEANERS
from langops.parser.utils.extractors import (
    extract_timestamp,
    extract_context_id,
    extract_metadata,
)


class Extractor:
    timestamp = staticmethod(extract_timestamp)
    context_id = staticmethod(extract_context_id)
    metadata = staticmethod(extract_metadata)


__all__ = ["PatternResolver", "STAGE_NAME_CLEANERS", "Extractor"]
