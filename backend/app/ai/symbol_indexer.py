"""
Symbol Indexer

Author: Harsh Aryan
Project: Cognisys
"""

from pathlib import Path

from app.parser.symbol_extractor import SymbolExtractor


class SymbolIndexer:
    """
    Converts repository symbols into searchable
    symbol-level chunks.
    """

    def __init__(self, repository_path):

        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise ValueError(
                "Repository path does not exist."
            )

        if not self.repository_path.is_dir():
            raise ValueError(
                "Repository path must be a directory."
            )

        self.symbol_extractor = SymbolExtractor()

    def create_symbol_chunks(self):

        symbols = self.symbol_extractor.extract(
            str(self.repository_path)
        )

        repository_name = self.repository_path.name

        chunks = []

        for source, file_symbols in symbols.items():

            # -----------------------------
            # Classes
            # -----------------------------

            for symbol in file_symbols["classes"]:

                chunks.append(
                    {
                        "content": symbol["code"],
                        "metadata": {
                            "repository": repository_name,
                            "source": source,
                            "symbol_id": symbol["id"],
                            "symbol_name": symbol["name"],
                            "symbol_type": symbol["type"],
                            "line": symbol["line"],
                            "line_end": symbol["end_line"],
                            "parent_class": None,
                        },
                    }
                )

            # -----------------------------
            # Functions / Methods
            # -----------------------------

            for symbol in file_symbols["functions"]:

                chunks.append(
                    {
                        "content": symbol["code"],
                        "metadata": {
                            "repository": repository_name,
                            "source": source,
                            "symbol_id": symbol["id"],
                            "symbol_name": symbol["name"],
                            "symbol_type": symbol["type"],
                            "line": symbol["line"],
                            "line_end": symbol["end_line"],
                            "parent_class": symbol["parent_class"],
                        },
                    }
                )

        return chunks