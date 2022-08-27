import logging
import os
from types import SimpleNamespace

import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from src.phockup import Phockup

logger = logging.getLogger('phockup')


def setup_logging(options: SimpleNamespace):
    """Configure logging."""
    root = logging.getLogger('')
    root.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    root.addHandler(ch)
    if not options.quiet ^ options.progress:
        logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    if options.log:
        logfile = os.path.expanduser(options.log)
        fh = logging.FileHandler(logfile)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    logger.debug("Debug logging output enabled.")
    logger.debug("Running Phockup version %s", options.version)


def get_config_options(arg_options=None, default_config_path=None) -> SimpleNamespace:
    if arg_options.config_file is None and os.path.exists(default_config_path):
        # None specified, but default exists on disk
        logger.info(f"Found default configuration file {default_config_path}. Loading...")
        return load_config(default_config_path)
    elif arg_options.config_file:
        # Load specified
        logger.info(f"Loading configuration from {arg_options.config_file}...")
        return load_config(arg_options.config_file)
    else:
        # Empty Config
        return SimpleNamespace()


def read_yaml(file_path):
    """
    YAML loading routine that checks for existence of the file specified
    and then parses it using `safe_load` to prevent malicious payloads.

    If the specified configuration file does not exist, FileNotFoundError
    error will be raised
    """
    # TODO: Update to validate file is YAML, possibly
    #  via https://yamllint.readthedocs.io/en/stable/development.html

    if file_path is not None:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    return yaml.safe_load(f)
                except (ParserError, ScannerError) as e:
                    raise RuntimeError(f"Invalid YAML in {file_path}.  Please verify syntax of YAML content.") from e
                except Exception as e:
                    logger.exception(e)
                    logger.warning(type(e))

        else:
            raise FileNotFoundError(f"Specified configuration file {file_path} does not exist")


def load_config(config_file_path) -> Phockup.Config:
    """
    Configuration file parsing used to set or override default values and return a Namespace
    """
    phockup_config = read_yaml(config_file_path)
    if phockup_config:
        logger.info(f"Loaded configuration from {config_file_path}")
    else:
        logger.warning(f"No configuration details found in {config_file_path}")
        phockup_config = {}
    # Use a Namespace for compatibility with argparse.  Store reference to the filepath
    config = Phockup.Config(config_file=config_file_path)

    # Load all supported configuration options
    config.ignore_files = phockup_config.get("ignored-files")

    return config


def merge_options(defaults: SimpleNamespace, overrides: SimpleNamespace) -> SimpleNamespace:
    """
    Merge two namespaces, overriding the values in the 'defaults'
    namespace with those provided in the overrides that have key
    collisions.  The resulting namespace will have the superset of the
    two provided collections
    """
    options = vars(defaults)
    options.update(vars(overrides))
    return SimpleNamespace(**options)


