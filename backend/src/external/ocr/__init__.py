from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Ocr(ABC):
    """
    Interface for scanning S3 URLs.
    Defines the contract that any S3 scanner implementation must fulfill.
    """

    @abstractmethod
    def scan(self, s3_url: str) -> dict[str, Any]:
        """
        Scan an S3 URL and return metadata about the object.

        Args:
            s3_url: The S3 URL to scan (format: s3://bucket-name/key)

        Returns:
            Dictionary containing metadata about the S3 object

        Raises:
            ValueError: If the URL format is invalid
        """
        pass
