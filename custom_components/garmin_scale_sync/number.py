"""Sensor platform for Garmin Scale Sync integration."""
from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    SUFFIX_BODYFAT,
    SUFFIX_MUSCLEWEIGHT,
    SUFFIX_VICERALFAT,
    SUFFIX_WEIGHT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Initialize Garmin Scale Sync config entry."""
    # unique_id = config_entry.entry_id
    # unique_id = f"{config_entry.entry_id}_{SensorStateClass.MEASUREMENT}"
    # {self.unique_id}_{SensorStateClass.MEASUREMENT}
    base_unique_id = config_entry.entry_id

    async_add_entities(
        [
            WeightEntry(base_unique_id, SUFFIX_WEIGHT),
            BodyFat(base_unique_id, SUFFIX_BODYFAT),
            MuscleWeight(base_unique_id, SUFFIX_MUSCLEWEIGHT),
            ViceralFat(base_unique_id, SUFFIX_VICERALFAT),
        ]
    )


class GarminScaleBaseEntity(NumberEntity):
    """Base Entity for all Garmin Scale Sync entities."""

    def __init__(
        self,
        base_unique_id: str,
        entity_suffix: str,
        name: str,
        max_value: float,
        min_value: float,
        default_value: float,
        unit_of_measurement: str,
    ) -> None:
        super().__init__()
        self._attr_name = entity_suffix
        self._attr_unique_id = f"{base_unique_id}_{entity_suffix}"
        self._attr_mode = NumberMode.BOX
        self._attr_native_max_value = max_value
        self._attr_native_min_value = min_value
        self._attr_native_value = default_value
        self._attr_step = 0.01
        self._attr_unit_of_measurement = unit_of_measurement
        self.entryID = base_unique_id

    # async def async_registry_entry_updated(self) -> None:
    #     self.hass.data[DOMAIN, self._attr_unique_id] = self._attr_native_value
    #     self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.hass.data[DOMAIN, self._attr_unique_id] = value
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entryID)},
            "name": "Garmin Scale Sync",
            "manufacturer": DOMAIN,
        }


class WeightEntry(GarminScaleBaseEntity):
    """Entity to input body weight in KG."""

    def __init__(self, base_unique_id: str, entity_suffix: str) -> None:
        super().__init__(
            base_unique_id, entity_suffix, "Weight Entry", 500.0, 0.0, 50.0, "kg"
        )
        self._attr_device_class = NumberDeviceClass.WEIGHT


class BodyFat(GarminScaleBaseEntity):
    """Entity to input body fat in percentage."""

    def __init__(self, base_unique_id: str, entity_suffix: str) -> None:
        super().__init__(
            base_unique_id, entity_suffix, "Body Fat", 100.0, 0.0, 20.0, "%"
        )


class MuscleWeight(GarminScaleBaseEntity):
    """Entity to input muscle weight in percentage."""

    def __init__(self, base_unique_id: str, entity_suffix: str) -> None:
        super().__init__(
            base_unique_id, entity_suffix, "Muscle Weight", 500.0, 0.0, 50.0, "%"
        )


class ViceralFat(GarminScaleBaseEntity):
    """Entity to input visceral fat value."""

    def __init__(self, base_unique_id: str, entity_suffix: str) -> None:
        super().__init__(
            base_unique_id, entity_suffix, "Visceral Fat", 100.0, 0.0, 10.0, "%"
        )
