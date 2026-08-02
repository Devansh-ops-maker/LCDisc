import discord

class TeamInviteView(discord.ui.View):
    def __init__(self, invited_user):
        super().__init__(timeout=60)
        self.invited_user = invited_user
        self.accepted = None

    @discord.ui.button(label="Accept",
                       style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.invited_user:
            await interaction.response.send_message(
                "This invitation isn't for you.",
                ephemeral=True
            )
            return

        self.accepted = True

        await interaction.response.send_message(
            "You accepted the invitation!"
        )

        self.stop()
    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.invited_user:
            await interaction.response.send_message(
                "This invitation isn't for you.",
                ephemeral=True
            )
            return

        self.accepted = False

        await interaction.response.send_message(
            "You declined the invitation."
        )

        self.stop()