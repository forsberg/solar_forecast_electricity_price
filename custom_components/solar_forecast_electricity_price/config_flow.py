"""Config flow for the PriceWithSolarintegration."""

from homeassistant.const import CONF_NAME
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    DeviceSelector,
    DeviceFilterSelectorConfig,
)
from homeassistant import config_entries
from homeassistant.util import slugify
from homeassistant.core import callback
from typing import Any
import logging

import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_GRID_IMPORT_COST_SENSOR,
    CONF_POWER_DRAW,
    CONF_GRID_EXPORT_INCOME_SENSOR,
    CONF_SOLAR_FORECAST,
)

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_GRID_IMPORT_COST_SENSOR): EntitySelector(
            EntitySelectorConfig(domain="sensor", multiple=False)
        ),
        vol.Required(CONF_GRID_EXPORT_INCOME_SENSOR): EntitySelector(
            EntitySelectorConfig(domain="sensor", multiple=False)
        ),
        vol.Required(CONF_POWER_DRAW): int,
        vol.Required(CONF_SOLAR_FORECAST): DeviceSelector(
            DeviceFilterSelectorConfig(multiple=True)
        ),
    }
)


class PriceWithSolarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            if len(user_input.get(CONF_NAME, "")) == 0:
                errors["base"] = CONF_NAME

            await self.async_set_unique_id(slugify(user_input[CONF_NAME]))
            self._abort_if_unique_id_configured()
            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "PriceWithSolarOptionsFlowHandler":
        """Create the options flow."""
        return PriceWithSolarOptionsFlowHandler()


class PriceWithSolarOptionsFlowHandler(config_entries.OptionsFlowWithReload):
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        if user_input is not None:
            _LOGGER.info(f"user_input {user_input}")
            return self.async_create_entry(data=user_input)

        _LOGGER.info(
            f"config_entry options: {self.config_entry.options}, config_entry.data {self.config_entry.data}"
        )

        return self.async_show_form(
            step_id="init",
            # Read values first from config.data, then override
            # with values from config.options
            data_schema=self.add_suggested_values_to_schema(
                self.add_suggested_values_to_schema(
                    CONFIG_SCHEMA, self.config_entry.data
                ),
                self.config_entry.options,
            ),
            last_step=True,
        )
