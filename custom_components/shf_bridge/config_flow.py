# Copyright (C) 2026 LoeLabs LLC - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# ~
"""Config flow for Smart Home Floorplan Bridge integration."""
from __future__ import annotations

from homeassistant import config_entries  # pylint: disable=import-error
from homeassistant.data_entry_flow import FlowResult  # pylint: disable=import-error
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class SmartHomeFloorplanBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore[call-arg,misc]
    """Handle a config flow for Smart Home Floorplan Bridge."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        
        _LOGGER.info("Config flow: User step initiated")
        
        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            # No configuration needed, just create the entry
            _LOGGER.info("Config flow: Creating entry for Smart Home Floorplan")
            return self.async_create_entry(title="Smart Home Floorplan", data={})

        _LOGGER.info("Config flow: Showing form to user")
        return self.async_show_form(step_id="user")
