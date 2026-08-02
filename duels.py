import os
import asyncio
from database import session
from dotenv import load_dotenv
from ques_checks import get_problem,check_question

load_dotenv()

DuelTime=int(os.getenv("DUEL_TIME"))
SleepTime=int(os.getenv("SLEEP_TIME"))
TotalChecks=int(os.getenv("TOTAL_CHECKS"))
q1score=int(os.getenv("Q1score"))
q2score=int(os.getenv("Q2score"))
q3score=int(os.getenv("Q3score"))



message1="A duel match has been started between {} vs {}. The match will begin shortly.\n {}"

message2 = """
                TEAM DUEL 

{}  vs  {}

Time Limit: {}

Problems:
Q1. {}   (3 points)
Q2. {}   (5 points)
Q3. {}   (7 points)
\n
{}
"""

message3="Ques{} has been solved by the opponent team, it is no longer available for score.\n {}"

message4="The duel has been completed.\n\n The score of {} was {} vs The score of the {} was {}.\n\n.The winner of the duel is {}.\n {}"

async def duels(ctx,TeamName1: str,TeamName2: str):

    query1="""SELECT TeamSize,TeamLeader,Mem1,Mem2,Mem3 FROM LCDisc.Teams
    WHERE TeamName=%s
    """

    check1=session.execute(query1,(TeamName1,)).one()

    query2="""SELECT TeamSize,TeamLeader,Mem1,Mem2,Mem3 FROM LCDisc.Teams
    WHERE TeamName=%s
    """

    check2=session.execute(query2,(TeamName2,)).one()

    if check1 and check2:
        if TeamName1==TeamName2:
            await ctx.send("Teams can not duel with themselved.")
            return
        else:
            T1size=check1.TeamSize
            T2size=check2.TeamSize
            T1dis={}
            T2dis={}
            T1leet={}
            T2leet={}

            T1leet["Mem1"]=check1.TeamLeader
            T2leet["Mem1"]=check2.TeamLeader

            queryT1="""SELECT author FROM LCDisc.Users
            WHERE username=%s
            """

            T1dis["Mem1"]=session.execute(queryT1,(T1leet["Mem1"]),).one()

            queryT2="""SELECT author FROM LCDisc.Users
            WHERE username=%s
            """

            T2dis["Mem1"]=session.execute(queryT2,(T2leet["Mem1"]),).one()


            for i in range(1,T1size):
                T1leet[f"Mem{i+1}"]=getattr(check1,f"Mem{i}")

                querydisc="""SELECT author FROM LCDisc.Users
                WHERE username=%s
                """

                T1dis[f"Mem{i+1}"]=session.execute(querydisc,(T1leet[f"Mem{i+1}"]),).one()

            for i in range(1,T2size):
                T2leet[f"Mem{i+1}"]=getattr(check2,f"Mem{i}")

                querydisc="""SELECT author FROM LCDisc.Users
                WHERE username=%s
                """

                T2dis[f"Mem{i+1}"]=session.execute(querydisc,(T2leet[f"Mem{i+1}"]),).one()

            all_members=list(T1dis.values())+list(T2dis.values())

            mentions = " ".join(f"<@{row.author}>" for row in all_members)

            await ctx.send(message1.format(TeamName1,TeamName2,mentions))

            ques1=await get_problem("Easy")
            ques2=await get_problem("Medium")
            ques3=await get_problem("Hard")

            await ctx.send(message2.format(TeamName1,TeamName2,DuelTime,ques1["title"],ques2["title"],ques3["title"],mentions))

            T1score,T2score=await monitorduel(T1dis,T2dis,T1leet,T2leet,ques1["url"],ques2["url"],ques3["url"],ctx)

            if T1score>T2score:
                winner=TeamName1
            else:
                winner=TeamName2

            await ctx.send(message4.format(TeamName1,T1score,TeamName2,T2score,winner,mentions))
            return
    else:
        print("Team does not exists.Can not start a duel.")
        return 
async def monitorduel(T1dis,T2dis,T1leet,T2leet,ques1,ques2,ques3,ctx):

    total_ques=3
    solvedques=set()
    questions=[
        ques1,
        ques2,
        ques3,
    ]

    scores={
        1:q1score,
        2:q2score,
        3:q3score
    }

    T1ques={}
    T1score=0
    T2ques={}
    T2score=0

    for quesindx in range(1,total_ques+1):
        T1ques[f"Ques{quesindx}"]=float('inf')
        T2ques[f"Ques{quesindx}"]=float('inf')
    

    for check in range(TotalChecks):
        if (len(solvedques)==total_ques):
            break
        for quesindx in range(1,total_ques+1):
            if quesindx in solvedques:
                continue
            for memindx in range(1,len(T1leet)+1):
                timestamp=await check_question(T1leet[f"Mem{memindx}"],questions[quesindx-1])
                if timestamp is not None:
                 T1ques[f"Ques{quesindx}"]=min(T1ques[f"Ques{quesindx}"],timestamp)

            for memindx in range(1,len(T2leet)+1):
                timestamp=await check_question(T2leet[f"Mem{memindx}"],questions[quesindx-1])
                if timestamp is not None:
                 T2ques[f"Ques{quesindx}"]=min(T2ques[f"Ques{quesindx}"],timestamp)

            if T1ques[f"Ques{quesindx}"]<T2ques[f"Ques{quesindx}"]:
                solvedques.add(quesindx)
                T1score+=scores[quesindx]
                await ping(T2dis,quesindx,ctx)
            elif T1ques[f"Ques{quesindx}"]>T2ques[f"Ques{quesindx}"]:
                solvedques.add(quesindx)
                T2score+=scores[quesindx]
                await ping(T1dis,quesindx,ctx)
        await asyncio.sleep(SleepTime)
    return (T1score,T2score)
async def ping(Teamdis,quesno,ctx):

    all_members=list(Teamdis.values())

    mentions = " ".join(f"<@{row.author}>" for row in all_members)

    await ctx.send(message3.format(quesno,mentions))



    
            
