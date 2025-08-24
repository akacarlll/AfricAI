from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
import pandas as pd
from typing import Any, Dict


class ColumnVerifierHook:
    def __init__(self):
        self.conf_catalog = None

    @hook_impl
    def after_catalog_created(
        self, catalog: DataCatalog, conf_catalog: Dict[str, Any]
    ) -> None:
        """
        Store the catalog configuration after the catalog is created.
        """
        self.conf_catalog = conf_catalog

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, data: Any) -> None:
        """
        Verify the columns of the loaded dataset against the expected columns defined in the catalog.
        """
        if self.conf_catalog is None:
            raise RuntimeError(
                "Catalog configuration not set. Ensure 'after_catalog_created' hook is called first."
            )

        dataset_config = self.conf_catalog.get(dataset_name, {})
        expected_columns = dataset_config.get("metadata", {}).get(
            "expected_columns", None
        )

        if expected_columns is None:
            return

        if not isinstance(data, pd.DataFrame):
            return

        actual_columns = data.columns.tolist()

        if not set(expected_columns).issubset(set(actual_columns)):
            raise ValueError(
                f"Columns mismatch for dataset '{dataset_name}'. Expected at least:{expected_columns}, Got: {actual_columns}"
            )
