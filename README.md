# LCDisc

LCDisc is a Discord bot built for the competitive programming community, bringing LeetCode directly into Discord. It allows users to verify their LeetCode accounts, discover practice problems, and compete in both team duels and multiplayer contests without leaving their server.

## Features

- **LeetCode Account Verification**
  - Securely links a user's Discord account with their LeetCode profile.

- **Problem Recommendation**
  - Recommends a random LeetCode problem based on the requested difficulty level.

- **Team Management**
  - Create teams, invite members, and manage team rosters directly from Discord.

- **Team Duels**
  - Organize head-to-head matches between two teams. Teams race to solve a set of problems, with points awarded to the team that solves each problem first.

- **Multiplayer Matches**
  - Create contests where multiple teams compete simultaneously. Teams are ranked based on their total score, with submission times used as a tiebreaker.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/LCDisc.git
cd LCDisc
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
```

Activate it:

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project directory and add the required configuration.

Example:

```env
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN

RANDOM_STRING_LENGTH=8
REGISTER_TIMEOUT=45

MATCH_TIME=2
DUEL_TIME=40

Q1score=3
Q2score=5
Q3score=7
```

### 5. Set up Cassandra

Create the required keyspace and tables before running the bot.

### 6. Start the bot

```bash
python3 main.py
```

---

## Commands

### User Commands

| Command | Description |
|---------|-------------|
| `!register <leetcode_username>` | Verify and link your LeetCode account. |
| `!unregister` | Remove the linked LeetCode account. |
| `!recommend <easy/medium/hard>` | Get a random LeetCode problem. |

### Team Commands

| Command | Description |
|---------|-------------|
| `!createTeam <team_name>` | Create a new team. |
| `!addMember <team_name> @member` | Invite a verified user to your team. |
| `!removeMember <team_name> @member` | Remove a member from your team. |
| `!duels <team1> <team2>` | Start a duel between two teams. |

### Match Commands

| Command | Description |
|---------|-------------|
| `!createMatch <match_name>` | Create a new match. *(Admin only)* |
| `!registerMatch <match_name> <team_name>` | Register a team for a match. |
| `!startMatch <match_name>` | Start a registered match. *(Admin only)* |

### Help

| Command | Description |
|---------|-------------|
| `!help` | Display all available commands and their usage. |

---
