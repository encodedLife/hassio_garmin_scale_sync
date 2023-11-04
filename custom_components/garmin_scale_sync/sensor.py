# """Sensor platform for Garmin Scale Sync integration."""
# from __future__ import annotations

# from homeassistant.components.sensor import SensorEntity
# from homeassistant.components.number import NumberEntity, NumberMode, NumberDeviceClass
# from homeassistant.components.input_number import InputNumber, CONF_ICON
# from homeassistant.config_entries import ConfigEntry
# from homeassistant.const import CONF_ENTITY_ID
# from homeassistant.core import HomeAssistant
# from homeassistant.helpers import entity_registry as er
# from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from homeassistant.helpers.typing import ConfigType


# async def async_setup_entry(
#     hass: HomeAssistant,
#     config_entry: ConfigEntry,
#     async_add_entities: AddEntitiesCallback,
# ) -> None:
#     """Initialize Garmin Scale Sync config entry."""
#     registry = er.async_get(hass)
#     # Validate + resolve entity registry id to entity_id
#     # entity_id = er.async_validate_entity_id(
#     #     # registry, config_entry.options[CONF_ENTITY_ID]
#     # )
#     # TODO Optionally validate config entry options before creating entity
#     name = config_entry.title
#     unique_id = config_entry.entry_id

#     # async_add_entities(
#     #     [
#     #         # testInputNumb(),
#     #         # garmin_scale_syncSensorEntity(unique_id, name, entity_id),
#     #         testNumberEntity("testunique", "testname", "asdfasd"),
#     #         # testInputNumb(),
#     #     ]
#     # )


# class garmin_scale_syncSensorEntity(SensorEntity):
#     """garmin_scale_sync Sensor."""

#     def __init__(self, unique_id: str, name: str, wrapped_entity_id: str) -> None:
#         """Initialize garmin_scale_sync Sensor."""
#         super().__init__()
#         self._wrapped_entity_id = wrapped_entity_id
#         self._attr_name = name
#         self._attr_unique_id = unique_id


# # Definieren Sie zuerst den ConfigType (wie zuvor besprochen)
# # ConfigType = Dict[str, Any]

# # # Erstellen Sie ein Konfigurationswörterbuch
# # config = {
# #     CONF_INITIAL: 5.0,  # Anfangswert
# #     CONF_MIN: 0.0,      # Minimaler Wert
# #     CONF_MAX: 10.0,     # Maximaler Wert
# #     CONF_STEP: 0.5,     # Schrittweite
# #     CONF_NAME: "My Slider",       # Optional: Name des Sliders
# #     CONF_ICON: "mdi:volume-high", # Optional: Icon
# #     CONF_UNIT_OF_MEASUREMENT: "Units", # Optional: Einheit der Messung
# #     CONF_ID: "unique_id_12345",   # Optional: Eindeutige ID
# #     CONF_MODE: "default_mode"     # Optional: Modus
# # }

# # class testInputNumb(InputNumber):
# #     def __init__(self, config: ConfigType) -> None:
# #         super().__init__(config)
# #         self._attr_name = "inpNum"
# #         self._attr_unique_id = "asdfaaasdf"
# #         self._minimum = 0.00
# #         self._maximum = 300.00
# #         self._step = 0.01
# #         self.editable = True


# class testNumberEntity(NumberEntity):
#     """garmin_scale_sync Sensor."""

#     def __init__(
#         self,
#         unique_id: str,
#         name: str,
#         wrapped_entity_id: str,
#     ) -> None:
#         """Initialize garmin_scale_sync Sensor."""
#         super().__init__()
#         self._wrapped_entity_id = wrapped_entity_id
#         self._attr_name = name
#         self._attr_unique_id = unique_id
#         self._attr_mode = NumberMode.BOX
#         self._attr_native_max_value = 300.00
#         self._attr_native_min_value = 0.00
#         self._attr_native_step = 0.01
#         self._attr_native_value = 50.0
#         self._attr_device_class = NumberDeviceClass.WEIGHT

#         # Implement one of these methods.

#     def set_native_value(self, value: float) -> None:
#         """Update the current value."""
#         self._attr_native_value = value
#         self.async_write_ha_state()

#     async def async_set_native_value(self, value: float) -> None:
#         """Update the current value."""
