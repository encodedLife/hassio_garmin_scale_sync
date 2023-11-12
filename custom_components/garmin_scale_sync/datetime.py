"""Sensor platform for Garmin Scale Sync integration."""
from __future__ import annotations

from datetime import datetime

from homeassistant.components.datetime import DateTimeEntity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, SUFFIX_MEASUREMENT_DATETIME


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize Garmin Scale Sync config entry."""
    base_unique_id = config_entry.entry_id
    async_add_entities(
        [
            GarminDateTimeInput(base_unique_id, SUFFIX_MEASUREMENT_DATETIME),
        ]
    )


class GarminDateTimeInput(DateTimeEntity):
    """Entity for date input."""

    def __init__(self, base_unique_id: str, entity_suffix: str) -> None:
        self._attr_name = entity_suffix
        self._attr_icon = "mdi:calendar"
        self._attr_unique_id = f"{base_unique_id}_{entity_suffix}"
        self._attr_has_date = True
        self._attr_has_time = True
        self._attr_native_value = dt_util.utcnow()
        self.datetime = dt_util
        self.entryID = base_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entryID)},
            "name": "Garmin Scale Sync",
            "manufacturer": DOMAIN,
        }

    @property
    def date(self):
        return self._attr_native_value

    @property
    def has_date(self):
        return self._attr_has_date

    @property
    def has_time(self):
        return self._attr_has_time

    async def async_set_value(self, value: datetime) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()
