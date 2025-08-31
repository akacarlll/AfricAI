"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

from .extras import ColumnVerifierHook


# Hooks are executed in a Last-In-First-Out (LIFO) order.
HOOKS = (ColumnVerifierHook(),)

from kedro.config import OmegaConfigLoader  # noqa: E402

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
    },
}
