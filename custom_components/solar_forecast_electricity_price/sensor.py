import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
)

from datetime import datetime
from zoneinfo import ZoneInfo

from homeassistant.helpers import device_registry

from homeassistant.const import (
    CONF_NAME,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    EVENT_COMPONENT_LOADED,
)

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.helpers.event import (
    async_track_state_change_event,
)

from homeassistant.components.energy.websocket_api import async_get_energy_platforms

from .const import (
    DOMAIN,
    CONF_POWER_DRAW,
    CONF_GRID_IMPORT_COST_SENSOR,
    CONF_GRID_EXPORT_INCOME_SENSOR,
    CONF_SOLAR_FORECAST,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .helpers.calculate_prices import calculate_prices
from .helpers.general import get_parameter

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):

    sensor = PriceWithSolar(
        hass,
        get_parameter(config_entry, CONF_NAME),
        get_parameter(config_entry, CONF_GRID_IMPORT_COST_SENSOR),
        get_parameter(config_entry, CONF_GRID_EXPORT_INCOME_SENSOR),
        get_parameter(config_entry, CONF_POWER_DRAW),
        get_parameter(config_entry, CONF_SOLAR_FORECAST),
    )

    async_add_entities([sensor])


def get_currency(hass: HomeAssistant):
    """Get the Home Assistant default currency."""
    currency = hass.config.currency
    if currency:
        _LOGGER.debug("Using Home Assistant default currency '%s'", currency)
        return currency

    _LOGGER.warning("No default currency set in Home Assistant")
    return None  # No default currency


class PriceWithSolar(SensorEntity):
    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.MONETARY
    # Do not write list attributes to database.
    _unrecorded_attributes = frozenset({"prices_today", "prices_tomorrow"})

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        import_cost_sensor_id: str,
        export_income_sensor_id: str,
        power_draw: int,
        solar_forecast_device_ids: list[str],
    ):
        super().__init__()
        self.hass = hass
        self._name = name

        self._forecast_loaded = False
        self._import_cost_sensor_id = import_cost_sensor_id
        self._export_income_sensor_id = export_income_sensor_id

        self._source_ids = [self._import_cost_sensor_id, self._export_income_sensor_id]
        self._power_draw = power_draw
        self._solar_forecast_device_ids = solar_forecast_device_ids
        self._solar_forecast_config_entries: list[ConfigEntry] = []
        self._solar_forecast_domains = set()

        self._attr_native_value = None
        self._prices_today = []
        self._prices_tomorrow = []

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}-{self._import_cost_sensor_id}-{self._name}-{self._power_draw}-cost"

    def is_forecasts_ready(self, domain):
        entries = self.hass.config_entries.async_entries(domain)
        for entry in entries:
            if entry.state != ConfigEntryState.LOADED:
                return False
        return True

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        dev_reg = device_registry.async_get(self.hass)

        self._unit_of_measurement = get_currency(self.hass)

        for device_id in self._solar_forecast_device_ids:
            device = dev_reg.async_get(device_id)

            config_entry_id = list(device.config_entries)[0]
            config_entry = self.hass.config_entries.async_get_entry(config_entry_id)

            self._solar_forecast_config_entries.append(config_entry)
            self._solar_forecast_domains.add(config_entry.domain)

        self.forecast_platforms = await async_get_energy_platforms(self.hass)

        # 1. Initial calculation attempt
        await self._update_from_sources()

        # 2. Subscribe to updates for all source entities
        # This returns a callback to unsubscribe, which async_on_remove handles
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._import_cost_sensor_id, self._export_income_sensor_id],
                self._handle_src_update,
            )
        )

        self.async_on_remove(
            self.hass.bus.async_listen(
                EVENT_COMPONENT_LOADED, self.component_loaded_listener
            )
        )

        _LOGGER.info(
            f"Found the following forecast_platforms: {self.forecast_platforms}"
        )

        dev_reg = device_registry.async_get(self.hass)

        return True

    async def _handle_src_update(self, event):
        """Update state when a source entity changes."""
        await self._update_from_sources()

    async def component_loaded_listener(self, event):
        """When component of solar forecast device has loaded, try updating sensor values"""
        if event.data["component"] in self._solar_forecast_domains:
            await self._update_from_sources()

    @property
    def available(self) -> bool:
        for entity_id in self._source_ids:
            state = self.hass.states.get(entity_id)
            # If any parent is unknown or unavailable, this entity is also unavailable
            if state is None or state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
                return False

        for config_entry in self._solar_forecast_config_entries:
            if config_entry.state != ConfigEntryState.LOADED:
                return False

        return True

    async def _update_from_sources(self):
        if not self.available:
            self._attr_native_value = None
            return

        import_cost_sensor = self.hass.states.get(self._import_cost_sensor_id)
        export_income_sensor = self.hass.states.get(self._export_income_sensor_id)

        forecasts = []

        zi = ZoneInfo(self.hass.config.time_zone)

        for config_entry in self._solar_forecast_config_entries:
            forecast = await self.forecast_platforms[config_entry.domain](
                self.hass, config_entry.entry_id
            )
            items = sorted(
                (datetime.fromisoformat(item[0]).astimezone(zi), item[1])
                for item in forecast["wh_hours"].items()
            )

            forecasts.append(items)

        priceinfo = calculate_prices(
            forecasts,
            datetime.now(tz=zi),
            import_cost_sensor.attributes["raw_today"],
            export_income_sensor.attributes["raw_today"],
            import_cost_sensor.attributes["raw_tomorrow"],
            export_income_sensor.attributes["raw_tomorrow"],
            self._power_draw,
        )

        self._attr_native_value = priceinfo.price_now
        self._prices_today = priceinfo.prices_today
        self._prices_tomorrow = priceinfo.prices_tomorrow

        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict:
        return {"prices_today": self._prices_today, "prices_tomorrow": self._prices_tomorrow}
