"""Sensor platform for Garmin Scale Sync integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import config_validation as cv, entity_platform


from .helper_methods import async_send_values_to_garmin
from .const import (
    DOMAIN,
    SUFFIX_BTN_SEND_DATA,
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
    base_unique_id = config_entry.entry_id

    async_add_entities(
        [SendValuesButton(base_unique_id, SUFFIX_BTN_SEND_DATA, hassHandler=hass)], True
    )

    platform = entity_platform.current_platform.get()
    # Services
    # platform.async_register_entity_service(
    #     "sync_weight",
    #     {vol.Required("weight"): cv.string},
    #     "async_press",
    # )

class SendValuesButton(ButtonEntity):
    """Entity to input body fat in percentage."""

    def __init__(
        self, base_unique_id: str, entity_suffix: str, hassHandler: HomeAssistant
    ) -> None:
        """Initialize the button."""
        self._attr_unique_id = f"{base_unique_id}_{entity_suffix}"
        self._attr_name = entity_suffix
        self._attr_icon = "mdi:send"
        self.hass = hassHandler
        self.entryID = base_unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.entryID)},
            "name": "Garmin Scale Sync",
            "manufacturer": DOMAIN,
        }

    async def async_press(self):
        """Handle the button press."""
        # get state of the number entities from the config entry

        # self.hass.async_add_executor_job(
        #     async_send_values_to_garmin, self.entryID, self.hass
        # )
        success = await async_send_values_to_garmin(self.entryID, self.hass)

        # self.hass.states.get("number.weight_entry").state

        # weight = self.hass.data[DOMAIN, f"{self.entryID}_{SUFFIX_WEIGHT}"]
        # body_fat = self.hass.data[DOMAIN, f"{self.entryID}_{SUFFIX_BODYFAT}"]
        # muscle_weight = self.hass.data[DOMAIN, f"{self.entryID}_{SUFFIX_MUSCLEWEIGHT}"]
        # visceral_fat = self.hass.data[DOMAIN, f"{self.entryID}_{SUFFIX_VICERALFAT}"]

        # weight = self.hass.config_entries.options[self.entryID]["weight"]
        # weight = self.hass.states.get("number.weight_entry").state
        # body_fat = self.hass.states.get("number.body_fat").state
        # muscle_weight = self.hass.states.get("number.muscle_weight").state
        # visceral_fat = self.hass.states.get("number.visceral_fat").state

        # Hier können Sie die ausgelesenen Werte weiterverarbeiten
        # Zum Beispiel:
        self.hass.components.persistent_notification.create(
            f"Sending Success: {success}",
            title="Garmin Scale Values",
        )
