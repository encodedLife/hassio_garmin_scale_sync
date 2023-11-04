"""Config flow for Garmin Scale Sync integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_ALIAS,
)

from homeassistant.data_entry_flow import FlowResult
from collections.abc import Mapping
from typing import Any, cast
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers import selector
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaFlowStep,
    SchemaConfigFlowHandler,
    SchemaOptionsFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)


from .const import DOMAIN, GSC_MUSCLEDATA_IN_PERCENT, GSC_OAUTH_TOKEN
import garth
from garth.exc import GarthException
import os

# Defining a fancy Form for popping up when an entry is added
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ALIAS): cv.string,  # used for the title of the entry
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(GSC_MUSCLEDATA_IN_PERCENT): cv.boolean,
    }
)


# define the Config flow for setup a new device Entry
CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA),
}


# getting the oauth token from garth
# this is done in a separate thread to not block the main thread
def get_oauth_token(username, password):
    try:
        garth.login(username, password)
        return garth.client.dumps()

    except GarthException as e:
        print(e.msg)
        return "Error"

    # garth.login(username, password)
    # return garth.client.dumps()


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config or options flow for Garmin Scale Sync."""

    VERSION = 1

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors or {},
        )

    async def async_step_user(self, user_input=None):
        """When a new device is created this method will be called"""
        # check if the user_input is None it means that no data was entered
        # so the form will be called
        if user_input is None:
            return await self._show_setup_form()
        else:
            # get the values from the form
            entryTitle = user_input[CONF_ALIAS]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            muscleDataIsPercent = user_input[GSC_MUSCLEDATA_IN_PERCENT]

            # get the oauth token from garth
            authToken = await self.hass.async_add_executor_job(
                get_oauth_token, username, password
            )

            if authToken == "Error":
                return await self._show_setup_form({"base": "invalid_auth"})

            return self.async_create_entry(
                title=entryTitle,
                data={
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                    GSC_MUSCLEDATA_IN_PERCENT: muscleDataIsPercent,
                    GSC_OAUTH_TOKEN: authToken,
                },
            )

        return self.async_abort(reason="Aborted")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return OptionsFlowHandler(config_entry=config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.current_config_entry = config_entry
        self.new_config_entry = config_entry
        super().__init__()

    @callback
    def finish_flow(self) -> FlowResult:
        """Update the ConfigEntry and finish the flow."""
        # after the user has changed the options
        # this method will be called and the config entry will be updated
        # with the new values
        # after this method the "config_entry_update_listener" method in __init__.py will be called
        # and the config entry will be reloaded therefore "async_unload_entry" will be called
        self.hass.config_entries.async_update_entry(
            self.current_config_entry,
            data=self.new_config_entry,
            title=self.new_config_entry[CONF_ALIAS],
        )
        return self.async_create_entry(title="", data={})

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options flow."""

        # check if there is a user_input if not the form will called
        if user_input is not None:
            # call update method for entry
            self.new_config_entry = user_input
            return self.finish_flow()

        # get the current config entry
        # for creating the options form
        mydict = self.current_config_entry.data

        # define the options schema and fill the default values with the current values in the config entry
        # if the user is not changing the values the current values will be used
        # to not allow empty values i set some fields to required
        options_flow_Schema = vol.Schema(
            {
                vol.Required(CONF_ALIAS, default=mydict.get(CONF_ALIAS)): cv.string,
                vol.Required(
                    CONF_USERNAME, default=mydict.get(CONF_USERNAME)
                ): cv.string,
                vol.Required(
                    CONF_PASSWORD, default=mydict.get(CONF_PASSWORD)
                ): cv.string,
                vol.Optional(
                    GSC_MUSCLEDATA_IN_PERCENT,
                    default=mydict.get(GSC_MUSCLEDATA_IN_PERCENT),
                ): cv.boolean,
            }
        )
        return self.async_show_form(step_id="init", data_schema=options_flow_Schema)


# @callback
# def finish_flow(self) -> FlowResult:
#     """Update the ConfigEntry and finish the flow."""
#     # new_data = self.current_config_entry | self.new_config_entry
#     self.hass.config_entries.async_update_entry(
#         self.current_config_entry,
#         data=self.new_config_entry,
#         title="testasldjföasjd",
#     )
#     return self.async_create_entry(title="", data={})
