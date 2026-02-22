# Smart Home Floorplan — Lovelace Card

**Transform your Home Assistant into a visual command center.**

Smart Home Floorplan is a 2D floorplan tool built for Home Assistant. Draw your home, place your devices, and see everything at a glance — lights, temperatures, door states, battery levels, and more — all on an interactive floorplan.

### Why?

I always wanted a nice floorplan view in Home Assistant, but drawing is not my thing — having to build it in Photoshop, SVG editors, or 3D modeling tools made it next to impossible. After many weekends trying to make my dashboard feel more like my house, I ended up building my own tool.

I wanted something that prioritized function and let me read the state of the house at a glance:

- Lights show brightness directly in the room
- Temperature shows as a subtle gradient
- Sensors show their state (e.g. "battery low")
- You can quickly see what's on, off, warm, open, etc.

It's still early, but it works as both a HA panel and a Lovelace card via an add-on.

[Website](https://getsmarthomefloorplan.com) · [Documentation](https://getsmarthomefloorplan.com/docs) · [Demo](https://getsmarthomefloorplan.com/demos) · [Discord](https://discord.gg/ScKGVyaCb7)

---

## What's in This Repo

This repository contains the **Smart Home Floorplan Lovelace card** — a custom frontend component that lets you embed your floorplan directly into any Home Assistant dashboard.

Use this when you want to see your floorplan alongside other cards on a dashboard, rather than only as a full-screen sidebar panel.

---

## Requirements

- Home Assistant 2023.1 or later
- The [Smart Home Floorplan add-on](https://github.com/loelabs-net/shf-ha-addons) installed and running
- [HACS](https://hacs.xyz/) (recommended for installation)

## Installation

> For the full step-by-step guide with screenshots, see the [Card Installation Docs](https://getsmarthomefloorplan.com/docs/home-assistant/cards).

You need to install **two** custom repositories to use the card: this one (the frontend card itself) and the [bridge integration](https://github.com/loelabs-net/shf-ha-integrations) (which enables non-admin access).

### Via HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. In HACS, click the **⋮** menu → **Custom repositories**
3. Add the first repository:
   - Repository: `https://github.com/loelabs-net/shf-ha-frontend`
   - Type: **Dashboard**
4. Add the second repository:
   - Repository: `https://github.com/loelabs-net/shf-ha-integrations`
   - Type: **Integration**
5. Close the dialog, then search for "Smart Home Floorplan" in HACS
6. Install both items, then restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/loelabs-net/shf-ha-frontend/releases)
2. Extract the files to your Home Assistant `config` directory
3. Restart Home Assistant

## Adding the Card to a Dashboard

1. Go to your Lovelace dashboard → click **⋮** → **Edit Dashboard**
2. Click **+ Add Card** → scroll down → **Manual**
3. The **Smart Home Floorplan** card should appear in the card picker

---

## Related Repositories

Smart Home Floorplan uses three repos for Home Assistant integration:

| Repository | Description |
|---|---|
| **[shf-ha-addons](https://github.com/loelabs-net/shf-ha-addons)** | Supervisor add-on — runs the floorplan service |
| **[shf-ha-frontend](https://github.com/loelabs-net/shf-ha-frontend)** | This repo — the Lovelace dashboard card |
| **[shf-ha-integrations](https://github.com/loelabs-net/shf-ha-integrations)** | Bridge integration enabling non-admin users to use floorplan cards |

---

## Support

- Join us on [Discord](https://discord.gg/ScKGVyaCb7) for help, feedback, and discussion
- Email: support@loelabs.net
- [Full Documentation](https://getsmarthomefloorplan.com/docs)

## License

Copyright © 2025 LoeLabs LLC. All rights reserved.

See [Terms of Use](https://getsmarthomefloorplan.com/terms) for details.
