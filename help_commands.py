async def bothelp(ctx,):
    registerhelp="! register followed by username will allow the bot to verify the leetcode id associated with user's dicord id."
    unregisterhelp="! unregister will help a user unregister the leetcode id associated with its discord id."
    recommendhelp="! recommend followed by difficulty will recommend the user a leetcode ques of the required difficulty."
    teamhelp1="! createTeam followed by TeamName will help you create a team of the desired teamname."
    addMemhelp="! addMember followed by TeamName,NewMem's discord will allow you to add a new member to the team."
    remMemhelp="! removeMember followed by TeamName,RemMem will allow you to remove a member from the team."
    duelHelp="! duels followed by the TeamName of both the teams in order will allow you to start a duel between the two teams."
    MatchHelp1="! createMatch followed by the MatchName  will allow you to create a match event."
    MatchHelp2="! registerMatch followed by MatchName and the TeamName will allow a team to register for a open match event."
    MatchHelp3="! startMatch followed by MatchName will allow you to start a match event."

    finMsg=registerhelp+"\n"+unregisterhelp+"\n"+recommendhelp+"\n"+teamhelp1+"\n"+addMemhelp+"\n"+remMemhelp+"\n"+duelHelp+"\n"+MatchHelp1+"\n"+MatchHelp2+"\n"+MatchHelp3

    await ctx.send(finMsg)
    return
async def adminCommands(ctx,):
    message="Only admin is allowed to use the createMatch and startMatch commands."

    await ctx.send(message)
    return 
async def flow(ctx,):
    message="""Any member is allowed to register their leetcode with their discord id.
               After verifying their id members can create a team together for participating in events.
               Team Leader can create the team,add members to the team or remove members from the team.
               A duel match can be started between any two teams.
               Admin is allowed to create a multi-team match.
               Teams can register for the match before its starting.
    """

    await ctx.send(message)
    return 

