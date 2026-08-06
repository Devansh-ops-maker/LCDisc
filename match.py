import asyncio
import os
from dotenv import load_dotenv
from database import session
from ques_checks import get_problem,check_question

load_dotenv()

q1score=int(os.getenv("Q1match"))
q2score=int(os.getenv("Q2match"))
q3score=int(os.getenv("Q3match"))
q4score=int(os.getenv("Q4match"))
q5score=int(os.getenv("Q5match"))
MatchTime=int(os.getenv("MATCH_TIME"))

mesmatch = """```text
MATCH STARTED
=============

Match
-----
{}

Time Limit
----------
{} hours

Problems
--------
Q1. {}   (3 points)
Q2. {}   (5 points)
Q3. {}   (7 points)
Q4. {}   (9 points)
Q5. {}   (11 points)
```"""

async def createMatch(ctx,Matchname: str):
    if ctx.author.guild_permissions.administrator:

        query1="""SELECT MatchName FROM LCDisc.Matches
        WHERE MatchName=%s
        """

        check=session.execute(query1,(Matchname,)).one()

        if check:
            await ctx.send("``` text A match with this match name already exists.Please try to create another match.```")
            return 
        else:
            query2="""Insert INTO LCDisc.Matches
            (MatchName)
            Values (%s)
            """

            session.execute(query2,(Matchname,))

            await ctx.send(f"``` text Match {Matchname} has been successfully created.```")
            return
    else:
        await ctx.send("``` text Only admin is allowed to create new messages.```")
        return
async def registerMatch(ctx,MatchName: str,TeamName: str):

    query1="""Select registeredTeams,started FROM LCDisc.Matches 
    WHERE MatchName=%s
    """

    check=session.execute(query1,(MatchName,)).one()

    if check:
        query2="""Select TeamLeader FROM LCDisc.Teams 
        WHERE TeamName=%s
        """

        check2=session.execute(query2,(TeamName,)).one()

        if check2:
            matchStarted=check.started
            if matchStarted:
                await ctx.send(f"``` text The match {MatchName} has already started.```")
                return
            else:
                registeredTeams=check.registeredTeams
                if registeredTeams is None:
                    registeredTeams=set()
                if TeamName in registeredTeams:
                    await ctx.send(f"``` text The team {TeamName} has already registered for the match {MatchName}```")
                    return 
                else:
                    registeredTeams.add(TeamName)

                    query3="""UPDATE LCDisc.Matches
                    SET registeredTeams=%s
                    WHERE MatchName=%s
                    """

                    session.execute(query3,(registeredTeams,MatchName,))

                    await ctx.send(f"``` text Registration of the team {TeamName} is successful for the match {MatchName}```")
                    return
        else:
            await ctx.send(f"``` text A Team of {TeamName} is not available.```")
            return 
    else:
        await ctx.send(f"``` text A Match of {MatchName} is not available.```")
        return
async def startMatch(ctx,MatchName: str):

    query1="""Select registeredTeams,started FROM LCDisc.Matches
    WHERE MatchName=%s
    """

    check=session.execute(query1,(MatchName,)).one()

    if check:
        registeredTeams=check.registeredTeams
        started=check.started

        if started:
            await ctx.send(f"``` text The match {MatchName} has already started.```")
            return
        else:
            if registeredTeams  and len(registeredTeams)>=2:
                await ctx.send(f"``` text Match {MatchName} is about to start!```")
                await ctx.send(f"``` text {len(registeredTeams)} teams have registered for the match! ```")
                message=f"The registered teams for {MatchName} are: "
                teamindx=1
                for team in registeredTeams:
                    message+="\n"
                    message += f"{teamindx}. {team}"
                    teamindx+=1
                await ctx.send(message)


                eques=await get_problem("Easy")
                mques1=await get_problem("Medium")
                mques2=await get_problem("Medium")
                mques3=await get_problem("Medium")
                hques=await get_problem("Hard")

                query2="""UPDATE LCDisc.Matches
                SET started=%s
                WHERE MatchName=%s
                """

                session.execute(query2,(True,MatchName,))

                questions=[
                    eques["url"],
                    mques1["url"],
                    mques2["url"],
                    mques3["url"],
                    hques["url"]
                ]
                question_scores=[
                    q1score,
                    q2score,
                    q3score,
                    q4score,
                    q5score
                ]

                await ctx.send(mesmatch.format(MatchName,MatchTime,eques["url"],mques1["url"],mques2["url"],mques3["url"],hques["url"]))

                await asyncio.sleep(MatchTime*60*60)

                teams=await calculatePoints(registeredTeams,questions,question_scores)

                await ctx.send("``` text The contest is over now.```")

                endmsg="The winning order of teams is: "

                for team in teams:
                    endmsg+=f"{team}.\n"

                await ctx.send(endmsg)
                return
            else:
                await ctx.send(f"``` text Atleast two teams are required for the {MatchName} to start.```")
                return
    else:
        await ctx.send("``` text No match by this name exists.```")
        return
async def calculatePoints(registeredTeams,questions,question_scores):

    scores={}

    for team in registeredTeams:
       queryteam="""SELECT TeamSize,TeamLeader,Mem1,Mem2,Mem3 FROM LCDisc.Teams
       WHERE TeamName=%s
       """

       checkteam=session.execute(queryteam,(team,)).one()

       solved=set()
       scores[team]={
           "scores":0,
           "timestamp":0
       }
       for ques in range(len(questions)):
           currques=questions[ques]
           score=question_scores[ques]
           timestamp=float('inf')
           for mem in range(checkteam.TeamSize):
               currmem=None
               if mem==0:
                   currmem=checkteam.TeamLeader
               else:
                   currmem=getattr(checkteam,f"Mem{mem}")

               memtime=await check_question(currmem,currques)

               if memtime is not None:
                   if ques not in solved:
                       scores[f"{team}"]["scores"]+=score
                       solved.add(ques)
                   timestamp=min(timestamp,memtime)
           if timestamp!=float('inf'):
               scores[f"{team}"]["timestamp"]+=timestamp

    sorted_teams = sorted(
    scores.keys(),
    key=lambda team: (-scores[team]["scores"], scores[team]["timestamp"])
    ) 

    return sorted_teams
    
               
                       
                   
                   
