# Copyright (C) 2026 LoeLabs LLC - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# ~
"""Proxy view for forwarding requests to the Smart Home Floorplan addon."""
from __future__ import annotations

from aiohttp import web  # pylint: disable=import-error
import logging
from typing import Any

from homeassistant.components.http import HomeAssistantView  # pylint: disable=import-error
from homeassistant.helpers import aiohttp_client  # pylint: disable=import-error

from .addon import get_addon_base_url
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _proxy_request(request: Any, path: str) -> web.Response:
    """Shared proxy implementation for forwarding requests to upstream addon."""
    _LOGGER.debug("PROXY REQUEST: %s", request)

    hass = request.app["hass"]
    # Get the aiohttp client session from Home Assistant helpers
    session = aiohttp_client.async_get_clientsession(hass)

    # Get the addon base URL dynamically (cached for 15 seconds)
    upstream_base = await get_addon_base_url(hass)
    upstream_url = f"{upstream_base}/{path}"

    # Forward body if present
    body = await request.read() if request.can_read_body else None

    # Forward selected headers
    headers = {}
    for h in (
        "Accept",
        "Content-Type",
        "If-None-Match",
        "If-Modified-Since",
        "Range",
        #"Authorization",  # only if your addon expects it
    ):
        if h in request.headers:
            headers[h] = request.headers[h]

    # Convert query parameters from MultiDict to dict for aiohttp
    query_params = dict(request.query) if request.query else None

    try:
        async with session.request(
            str(request.method),
            upstream_url,
            params=query_params,
            data=body,
            headers=headers,
            allow_redirects=False,
        ) as resp:
            # Strip hop-by-hop headers and content-encoding (aiohttp auto-decompresses)
            response_headers = {}
            for k, v in resp.headers.items():
                lk = k.lower()
                if lk in (
                    "connection",
                    "transfer-encoding",
                    "keep-alive",
                    "proxy-authenticate",
                    "proxy-authorization",
                    "te",
                    "trailers",
                    "upgrade",
                    "content-encoding",  # aiohttp auto-decompresses, body is already decoded
                    "content-length",    # length changed after decompression
                ):
                    continue
                response_headers[k] = v

            # 304 responses must not include a body
            data = b"" if resp.status == 304 else await resp.read()

            return web.Response(
                status=resp.status,
                headers=response_headers,
                body=data,
            )
    except Exception as e:  # pylint: disable=broad-exception-caught
        # Catching broad exception is acceptable here as we want to handle
        # any network or request errors and return a proper error response
        _LOGGER.exception("Error proxying request to %s: %s", upstream_url, e)
        return web.Response(status=500, text=f"Proxy error: {str(e)}")


class ShfBridgeProxy(HomeAssistantView):  # type: ignore[misc]
    """Proxy view for forwarding API requests to the addon."""

    url = "/api/" + DOMAIN + "/proxy/{path:.*}"
    name = "api:" + DOMAIN + ":proxy"
    requires_auth = True  # any logged-in HA user
    csrf_exempt = True

    async def get(self, request: Any, path: str) -> web.Response:
        """Handle GET requests."""
        return await _proxy_request(request, path)

    async def post(self, request: Any, path: str) -> web.Response:
        """Handle POST requests."""
        return await _proxy_request(request, path)

    async def put(self, request: Any, path: str) -> web.Response:
        """Handle PUT requests."""
        return await _proxy_request(request, path)

    async def delete(self, request: Any, path: str) -> web.Response:
        """Handle DELETE requests."""
        return await _proxy_request(request, path)

    async def head(self, request: Any, path: str) -> web.Response:
        """Handle HEAD requests."""
        return await _proxy_request(request, path)


class ShfBridgeStaticProxy(HomeAssistantView):  # type: ignore[misc]
    """Proxy view for forwarding static asset requests to the addon."""

    url = "/local/" + DOMAIN + "/proxy/{path:.*}"
    name = "local:" + DOMAIN + ":proxy"
    requires_auth = False  # static assets don't require auth
    csrf_exempt = True

    async def get(self, request: Any, path: str) -> web.Response:
        """Handle GET requests for static assets."""
        return await _proxy_request(request, path)
