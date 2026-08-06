import os
from database import session
from dotenv import load_dotenv
from discord import Member
from Views import TeamInviteView

load_dotenv()

MaxTeamSize=int(os.getenv("MAX_TEAM_SIZE"))

async def createTeam(ctx,TeamName: str):
    author=str(ctx.author.id)

    query1="""SELECT TeamLeader,TeamSize FROM LCDisc.Teams
    WHERE TeamName=%s
    """

    check=session.execute(query1,(TeamName,)).one()

    if check:
        TeamLeader=check.TeamLeader
        TeamSize=check.TeamSize

        await ctx.send(f"```text This Team already exist with {TeamLeader} as TeamLeader and the TeamSize is {TeamSize}```")
        return
    else:

        query2="""SELECT username FROM LCDisc.Users
        WHERE author=%s
        """

        check2=session.execute(query2,(author,)).one()

        if check2:
            LeadUsername=check2.username

            query3="""INSERT INTO LCDisc.Teams
            (TeamName,TeamLeader,TeamSize)
            VALUES (%s,%s,%s)
            """

            session.execute(query3,(TeamName,LeadUsername,1))

            await ctx.send(f"``` text Team  {TeamName} sucessfully created with {LeadUsername} as the TeamLeader.```")
            return 
        else:
            await ctx.send("``` text The username of the TeamLeader is not verified.Please first verify it.```")
            return
async def addMember(ctx,TeamName: str,NewMem :Member):
    author=str(ctx.author.id)

    query1="""SELECT TeamLeader,TeamSize FROM LCDisc.Teams
    WHERE TeamName=%s
    """

    check=session.execute(query1,(TeamName,)).one()

    if check:
        query2="""SELECT username FROM LCDisc.Users
        WHERE author=%s
        """

        check2=session.execute(query2,(author,)).one()

        if check2:
            LeadUsername=check.TeamLeader
            TeamSize=check.TeamSize
            AuthorUsername=check2.username

            if LeadUsername!=AuthorUsername:
                await ctx.send(f"``` text Only the TeamLeader {LeadUsername} is allowed to add members to the team.```")
                return
            else:
                if TeamSize==MaxTeamSize:
                    await ctx.send("``` text Team Size is already full, no more members can be added to the team.```")
                    return
                else:
                    query3="""SELECT username FROM LCDisc.Users
                    WHERE author=%s
                    """

                    check3=session.execute(query3,(NewMem.id,)).one()

                    if check3:
                        MemUsername=check3.username

                        view=TeamInviteView(NewMem)

                        await ctx.send(
                            f"{NewMem.mention}, you have been invited to Team {TeamName}.",
                            view=view
                        )

                        await view.wait()

                        if view.accepted is None:
                            await ctx.send("``` text Invitation timed out```")
                            return

                        if view.accepted:
                            column=f"Mem{TeamSize}"
                            query4=f"""UPDATE LCDisc.Teams 
                                   SET TeamSize=%s,{column}=%s
                                   WHERE TeamName=%s
                                   """
                            
                            session.execute(query4,(TeamSize+1,MemUsername,TeamName,))
                            
                            await ctx.send("``` text New member successfully added to the team.```")
                            return 
                        else:
                            await ctx.send("``` text The invitation has been declined.```")
                            return 
                    else:
                            await ctx.send(f"``` text The username of the new member {NewMem} is not verified```")
                            return
        else:
            await ctx.send(f"``` text The username is not verified for this id {author}.Please first verify it.```")
            return
    else:
        await ctx.send("This team does not exist")
        return 
async def removeMember(ctx,TeamName: str,RemMem: Member):

    author=str(ctx.author.id)

    query1="""SELECT TeamLeader FROM LCDisc.Teams
    WHERE TeamName=%s
    """

    check=session.execute(query1,(TeamName,)).one()

    if check:
        query2="""SELECT username FROM LCDisc.Users
        WHERE author=%s
        """

        check2=session.execute(query2,(author,)).one()

        if check2:
            LeaderUsername=check.TeamLeader
            AuthorUsername=check2.username

            if LeaderUsername==AuthorUsername:
                mems=[]

                query3="""SELECT Mem1,Mem2,Mem3 FROM LCDisc.Teams
                WHERE TeamName=%s
                """

                check3=session.execute(query3,(TeamName,)).one()
                if check3.Mem1 is not None:
                    mems.append(check3.Mem1)
                if check3.Mem2 is not None:
                    mems.append(check3.Mem2)
                if check3.Mem3 is not None:
                    mems.append(check3.Mem3)

                query4="""SELECT username FROM LCDisc.Users
                WHERE author=%s
                """

                check4=session.execute(query4,(RemMem.id,)).one()

                if check4:
                    MemUsername=check4.username

                    if LeaderUsername==MemUsername:
                        await ctx.send("``` text Team Leader can not be removed from the team.```")
                        return
                    else:
                        if MemUsername in mems:
                            mems.remove(MemUsername)
                            for i in range(len(mems)):

                                column=f"Mem{i+1}"
                                query5=f"""Update LCDisc.Teams
                                SET {column}=%s
                                WHERE TeamName=%s
                                """
                                session.execute(query5,(mems[i],TeamName))
                            column=f"Mem{len(mems)+1}"
                            query6=f"""UPDATE LCDisc.Teams
                            SET {column}=%s
                                TeamSize=%s
                            WHERE TeamName=%s
                            """

                            session.execute(query6,(None,len(mems)+1,TeamName,))

                            await ctx.send("``` text User is successfully removed from the Team.```")
                            return
                        else:
                            await ctx.send(f"``` text The member {RemMem.name} is not present in the Team {TeamName}```")
                            return
                else:
                    await ctx.send(f"``` text The member {RemMem.name} to be removed is not verified. ```")
                    return
            else:
                await ctx.send(f"``` text The user {author} is not allowed to remove members from the team {TeamName}```")
                return
        else:
            await ctx.send(f"``` text The username of the id {author} is not verified.Please verify it firs.```")
            return
    else:
        await ctx.send("``` text The team does not exist.```")
        return








