from abc import ABC, abstractmethod
from copy import deepcopy
from json import loads, dumps
from logging import Logger
from typing import Any, List, Optional
from .logging import setup_logger


class Flattener(ABC):
    @abstractmethod
    def flatten(self) -> str:
        pass


class PlanFlattener(Flattener):
    _plan: Any
    _logger: Logger

    def __init__(self, json_plan: str, logger: Optional[Logger] = None) -> None:
        self._plan = loads(json_plan)
        self._logger = (
            logger if logger is not None else setup_logger("plan-flattener", debug=True)
        )

    def _flatten_child_modules(self, modules: List) -> List:
        resources = []

        for module in modules:
            if "resources" in module.keys():
                for resource in module["resources"]:
                    resource_address = (
                        resource["address"]
                        if "address" in resource.keys()
                        else "unknown"
                    )
                    self._logger.debug(f"Adding resource: {resource_address}")
                    resources.append(deepcopy(resource))
            else:
                self._logger.debug("No resources found in child module")

            if "child_modules" in module.keys():
                resources.extend(self._flatten_child_modules(module["child_modules"]))
            else:
                self._logger.debug("No child modules found in module")

        return resources

    def _flatten_providers(self) -> List:
        providers = []

        if "configuration" in self._plan.keys():
            configuration = self._plan["configuration"]

            if "provider_config" in configuration.keys():
                provider_config = configuration["provider_config"]

                for provider in provider_config.values():
                    provider_name = (
                        provider["name"] if "name" in provider.keys() else "unknown"
                    )
                    self._logger.debug(f"Adding provider: {provider_name}")
                    providers.append(deepcopy(provider))
            else:
                self._logger.warning(
                    "Plan does not have 'provider_config' section under 'configuration'"
                )
        else:
            self._logger.warning("Plan does not have 'configuration' section")

        return providers

    def _flatten_resources(self) -> List:
        resources = []

        if "planned_values" in self._plan.keys():
            planned_values = self._plan["planned_values"]

            if "root_module" in planned_values.keys():
                root_module = planned_values["root_module"]

                if "resources" in root_module.keys():
                    for resource in root_module["resources"]:
                        resource_address = (
                            resource["address"]
                            if "address" in resource.keys()
                            else "unknown"
                        )
                        self._logger.debug(f"Adding resource: {resource_address}")
                        resources.append(deepcopy(resource))
                else:
                    self._logger.warning(
                        "Plan does not have 'resources' section under 'root_module'"
                    )

                if "child_modules" in root_module.keys():
                    child_modules_resources = self._flatten_child_modules(
                        root_module["child_modules"]
                    )
                    resources.extend(child_modules_resources)
                else:
                    self._logger.debug(
                        "Plan does not have 'child_modules' section under 'root_module'"
                    )
            else:
                self._logger.warning(
                    "Plan does not have 'root_module' section under 'planned_values'"
                )
        else:
            self._logger.warning("Plan does not have 'planned_values' section")

        return resources

    def flatten(self) -> str:
        self._logger.debug("Flattening providers")
        providers = self._flatten_providers()

        self._logger.debug("Flattening resources")
        resources = self._flatten_resources()

        return dumps({"providers": providers, "resources": resources})
