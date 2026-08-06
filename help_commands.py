async def bothelp(ctx):
    message = """```text
LCDisc Commands

!register <leetcode_username>
    Verify the LeetCode account associated with your Discord account.

!unregister
    Remove the linked LeetCode account from your Discord account.

!recommend <easy|medium|hard>
    Recommend a random LeetCode problem of the specified difficulty.

!createTeam <team_name>
    Create a new team.

!addMember <team_name> @member
    Invite a verified user to your team.

!removeMember <team_name> @member
    Remove a member from your team.

!duels <team1> <team2>
    Start a duel between two teams.

!createMatch <match_name>
    Create a new match event.

!registerMatch <match_name> <team_name>
    Register a team for an open match.

!startMatch <match_name>
    Start a match.
!flow
    To get the flow of the system.
!adminCommands
    To get the admin-only commands.
```"""

    await ctx.send(message)
async def adminCommands(ctx):
    message = """```text
Admin Commands

Only server administrators can use the following commands:

!createMatch <match_name>
!startMatch <match_name>
```"""

    await ctx.send(message)
async def flow(ctx):
    message = """```text
LCDisc Workflow

1. Register your LeetCode account using !register.

2. Create a team or join an existing team.

3. Team leaders can:
   • Create teams
   • Add members
   • Remove members

4. Teams can challenge each other using !duels.

5. Administrators can create multiplayer matches.

6. Teams register for a match before it starts.

7. Once the match begins, teams compete for the highest score.
```"""

    await ctx.send(message)
