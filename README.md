# Smart Home Floorplan Bridge

A Home Assistant custom integration that provides the Smart Home Floorplan Lovelace card and enables non-admin users to access addon information.

## Installation

### Via HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Go to **HACS** → **Integrations**
3. Click the three dots (⋮) in the top right
4. Select **Custom repositories**
5. Add this repository:
   - Repository: `https://github.com/loelabs-net/shf-ha-frontend`
   - Category: **Integration**
6. Click **Install** and restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/loelabs-net/shf-ha-frontend/releases)
2. Extract the `custom_components` folder to your Home Assistant `config` directory
3. Restart Home Assistant

## Adding the Card to Lovelace

1. Go to your Lovelace dashboard
2. Click the three dots (⋮) → **Edit Dashboard**
3. Click the **+** button to add a card
4. Click **+ ADD CARD** → Scroll down and click **MANUAL**
5. Add the following resource (if not already added):
   - **URL**: `/local/shf_bridge/shf-ha-frontend.js`
   - **Type**: `module`
6. The **Smart Home Floorplan** card should now be available in the card picker


## Requirements

- Home Assistant 2023.1 or later
- Smart Home Floorplan add-on installed and running
- HACS (for easy installation)


## License

Copyright © 2025 LoeLabs LLC. All rights reserved.