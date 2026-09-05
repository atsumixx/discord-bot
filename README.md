# Atsumi Piloting Services Discord Bot

A Discord bot for managing Genshin Impact commission services, specifically designed for exploration and maintenance commissions with an interactive ordering system.

## Features

- **Interactive Order System**: Users can place orders via `!order` command with dropdown selections and modal inputs
- **Exploration Services**: Commission pilots for map exploration across all Genshin Impact regions with dynamic pricing
- **Maintenance Services**: Artifacts and Talent building commissions
- **Custom Upgrades**: Character ascension and weapon upgrade services
- **Private Threads**: Each order gets a dedicated private thread for order management
- **Job Board**: Pilots can claim and manage jobs in the `#available-job` channel
- **Review System**: Completed orders automatically post reviews to `#done-deal✔️` with user avatars
- **Discount System**: 35% discount for exploration services when map is over 50% completed
- **Help Guide**: Comprehensive `!help` command with detailed usage instructions

## Commands

- `!help` - Displays the comprehensive guide to using the bot
- `!order` - Opens the interactive order menu to commission services

## Order Process

1. **Place Order**: Use `!order` to open the interactive cart
2. **Select Services**: 
   - Choose exploration regions (with 35% discount option for >50% completion)
   - Select maintenance services (Artifacts/Talent building)
   - Add custom upgrades (Character ascension/Weapon upgrades) via modals
3. **Submit**: Confirm your order to create a private thread and job posting
4. **Manage**: In your private thread:
   - Edit/replace your order if needed
   - Mark as resolved & review when completed
5. **Completion**: Reviews automatically post to `#done-deal✔️` with your avatar

## Setup Instructions

### Prerequisites
- Python 3.8+
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Discord token as an environment variable:
   ```bash
   set DISCORD_TOKEN=your_token_here  # Windows
   export DISCORD_TOKEN=your_token_here  # Linux/Mac
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

### Configuration

The bot uses the following configuration files:
- `config.py` - Contains pricing information for exploration and maintenance services
- `discloud.config` - Deployment configuration (if using Discloud hosting)

### Required Discord Channels
For full functionality, ensure your server has these channels:
- `#available-job` - Where job postings appear for pilots to claim
- `#done-deal✔️` - Where completed order reviews are posted

## Pricing

### Exploration Services
Standard rates vary by region (Mondstadt: $7.00, Liyue: $10.00, Inazuma: $25.00, etc.)
- **35% Discount**: Available when exploration is >50% complete

### Maintenance Services
- Artifacts Building: $1.50
- Talent Building 1-6: $0.50
- Talent Building 7-10: $2.00

### Custom Upgrades
- Character Ascension: $1.50 per ascension phase
- Weapon Upgrade: $1.50 per ascension phase

## How It Works

### For Clients
1. Use `!order` to open the interactive menu
2. Select desired services from dropdowns
3. Add custom upgrades using the blue buttons (opens modals)
4. Click "Confirm & Submit Order" to create a private thread and job posting
5. In your private thread, you can:
   - Edit your order if needed
   - Mark as resolved and leave a review when completed

### For Pilots
1. Monitor the `#available-job` channel for new job postings
2. Click "Claim Job" to assign yourself to a job
3. Click "Mark Resolved" when you've completed the commission
4. The client will then be prompted to leave a review

## Technology Stack

- **discord.py** - Python library for Discord API interaction
- **Python 3.8+** - Core programming language

## Files

- `main.py` - Main bot logic and command handlers
- `ui_components.py` - All interactive UI components (dropdowns, modals, views, buttons)
- `config.py` - Pricing configuration for services
- `discloud.config` - Deployment configuration
- `requirements.txt` - Python dependencies

## Notes

- The bot automatically deletes command messages to keep channels clean (requires manage messages permission)
- Private threads are created for each order to maintain privacy
- Job postings include role ping for Pilots (requires Pilot role to exist)
- Reviews are posted via webhook in `#done-deal✔️` to display user avatars
- Order sessions timeout after 3 minutes of inactivity

## Support

For issues or questions, please refer to the `!help` command within Discord or contact the bot administrator.

---

*Atsumi Piloting Services - Your trusted partner for Genshin Impact commission services*