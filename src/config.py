import os
from types import SimpleNamespace
from typing import Any

UNKNOWN = 'unknown'


class Config(SimpleNamespace):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Initialize all required keys in the configuration.  They key must *exist*
        # to avoid AttributeErrors and should be initialized to their default value
        self.input_dir = None
        self.output_dir = None
        self.dir_format = None

        self.date = None
        self.log = None
        self.file_type = None
        self.config_file = None

        self.date_field = "SubSecCreateDate SubSecDateTimeOriginal CreateDate DateTimeOriginal"
        self.debug: bool = os.environ.get('LOGLEVEL') == "DEBUG"
        self.dry_run: bool = False
        self.link: bool = False
        self.ignored_files: str = ".DS_Store, Thumbs.db"
        self.max_concurrency: int = 1
        self.max_depth: int = -1
        self.move: bool = False
        self.no_date_dir = UNKNOWN
        self.original_names: bool = False
        self.progress: bool = False
        self.quiet: bool = False
        self.regex = None
        self.skip_unknown: bool = False
        self.timestamp: bool = False
        self.version = None
