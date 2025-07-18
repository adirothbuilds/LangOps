import re
from datetime import datetime
from typing import Optional, Dict, Any, List


def extract_timestamp(line: str) -> Optional[datetime]:
    """
    Extracts a timestamp from a given line of text.
    Returns the timestamp in ISO 8601 format if found, otherwise returns None.

    Args:
        line (str): The line of text to search for a timestamp.

    Returns:
        Optional[str]: The extracted timestamp in ISO 8601 format, or None if no timestamp is found.
    """
    # Define multiple patterns to match different timestamp formats
    timestamp_patterns = [
        (
            r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?\b",
            ["%Y-%m-%d %H:%M:%S,%f", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"],
        ),
        (r"\b\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\b", ["%d/%b/%Y:%H:%M:%S"]),
        (r"\b\d{2}:\d{2}:\d{2}\b", ["%H:%M:%S"]),
        (r"\b\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\b", ["%Y/%m/%d %H:%M:%S"]),
    ]

    # Search for each pattern in the line
    for pattern, formats in timestamp_patterns:
        match = re.search(pattern, line)

        # If a match is found, try to parse it with the provided formats
        if match:
            raw_timestamp = match.group(0)
            for fmt in formats:
                try:
                    datetime_obj = datetime.strptime(raw_timestamp, fmt)
                    if datetime_obj.year == 1900:
                        now = datetime.now()
                        datetime_obj = datetime_obj.replace(
                            year=now.year, month=now.month, day=now.day
                        )
                    return datetime_obj
                except ValueError:
                    continue
    return None


def extract_context_id(
    lines: List[str], line_number: int, window: int = 20
) -> Optional[str]:
    """
    Extracts a context ID from a list of log lines around a specific line number.

    Args:
        lines (List[str]): The list of log lines.
        line_number (int): The line number to extract context from.
        window (int): The number of lines before and after the line number to consider.

    Returns:
        Optional[str]: The extracted context ID or None if not found.
    """

    def match_patterns(line: str) -> Optional[str]:
        """
        Matches the line against predefined patterns to extract context ID.

        Args:
            line (str): The line to match against patterns.

        Returns:
            Optional[str]: The matched context ID or None if no match is found.
        """
        for pattern in context_id_patterns:
            match = pattern.search(line)
            if match:
                value = match.group(1).strip()
                if (
                    len(value) >= 6
                    and not re.fullmatch(r"[a-z]{1,3}", value)
                    and not any(c in value for c in ["'", '"', "(", ")"])
                ):
                    return value
        return None

    def collect_context_lines(lines: List[str], start: int, end: int) -> List[str]:
        """
        Collects context lines that contain specific keywords.

        Args:
            lines (List[str]): The list of log lines.
            start (int): The starting index for the context window.
            end (int): The ending index for the context window.

        Returns:
            List[str]: A list of context lines containing the specified keywords.
        """
        return [
            line.strip()
            for line in lines[start:end]
            if any(kw in line.lower() for kw in keywords)
            and not re.match(r"^\[\d{4}-\d{2}-\d{2}", line)
        ]

    context_id_patterns = [
        re.compile(r"\b([a-fA-F0-9]{8,}[-:]?[a-fA-F0-9]{4,})\b"),
        re.compile(r"\bcontext[-_]?id[:=\s]?([a-zA-Z0-9-]{6,})\b", re.IGNORECASE),
        re.compile(r"\btrace[-_]?id[:=\s]?([a-zA-Z0-9-]{6,})\b", re.IGNORECASE),
        re.compile(r"\bFAIL\b\s+(src/[a-zA-Z0-9_/.-]+)", re.IGNORECASE),
        re.compile(r"\b(?:Exception|Error)[:=\s]+([a-zA-Z0-9_.-]+)", re.IGNORECASE),
    ]

    keywords = ["fail", "error", "exception", "trace", "context"]

    start = max(0, line_number - window - 1)
    end = min(len(lines), line_number + window)

    matches = [
        (i, match_patterns(lines[i].strip()))
        for i in range(start, end)
        if match_patterns(lines[i].strip())
    ]

    if matches:
        return sorted(
            matches, key=lambda x: (abs(x[0] - line_number), -len(x[1] or ""))
        )[0][1]

    context_lines = collect_context_lines(lines, start, end)
    if context_lines:
        return " | ".join(context_lines[:3])

    return None


def extract_metadata(data: str, source: Optional[str] = None) -> Dict[str, Any]:
    """
    Extracts metadata from the pipeline log data.

    Args:
        data (str): The raw log data from which to extract metadata.
        source (Optional[str]): The source of the pipeline logs (e.g., 'jenkins', 'github_actions').

    Returns:
        Dict[str, Any]: A dictionary containing extracted metadata such as build ID, triggered by user, branch, etc.
    """
    metadata = {}

    build_match = re.search(r"BUILD_ID=([^\s]+)", data)
    if build_match:
        metadata["build_id"] = build_match.group(1)

    user_match = re.search(r"Started by user (.+)", data)
    if user_match:
        metadata["triggered_by"] = user_match.group(1)

    branch_match = re.search(r"[Bb]ranch[:= ]+([^\s]+)", data)
    if branch_match:
        metadata["branch"] = branch_match.group(1)

    if source and "pipeline" in source.lower():
        metadata["pipeline_system"] = source.lower()

    first_ts = extract_timestamp(data)
    if first_ts:
        metadata["start_time"] = first_ts

    return metadata
