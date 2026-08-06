import os
from dotenv import load_dotenv
import uuid
import asyncio
from database import session
from user_checks import user_exists,check_readme


load_dotenv()

length=int(os.getenv("RANDOM_STRING_LENGTH"))
sleep_time=int(os.getenv("SLEEP_TIME1"))
message = """```text
Follow these steps to verify your LeetCode username.

1. Go to your LeetCode profile and click Edit Profile.
2. Change the "About Me" section to:

{}

Complete this within {} seconds.
```"""
async def register(ctx,username : str):
    author=str(ctx.author.id)

    query1="""SELECT username 
              FROM LCDisc.Users
              WHERE author=%s
           """
    check=session.execute(query1,(author,)).one()

    if check:
        user=check.username
        await ctx.send(f"```text User is already verified and is registered with the username {user} ```")
        return 
    else:
        if await user_exists(username):

            random_string=str(uuid.uuid4()).replace('-','')[:length]
            await ctx.send(message.format(random_string,sleep_time))
            await asyncio.sleep(sleep_time)
            changed_readme=await check_readme(username)

            if changed_readme==random_string:

                query2="""INSERT INTO LCDisc.Users
                (author,username)
                VALUES (%s,%s)
                """

                session.execute(query2,(author,username))

                await ctx.send("``` text The Leetcode username is successfully verified. ```")
                return
            else:
                await ctx.send("``` text The ReadMe does not match.Please try again. ```")
                return
        else:
            await ctx.send("``` text Wrong username entered.Please try again. ```")
            return
async def unregister(ctx,):
    author=str(ctx.author.id)

    query1="""SELECT username
    FROM LCDisc.Users 
    WHERE author=%s
    """

    check=session.execute(query1,(author,)).one()

    if check:

        query2="""DELETE FROM LCDisc.Users
        WHERE author=%s
        """

        session.execute(query2,(author,))


        await ctx.send("``` text User successfully unregistered. ```")
        return
    else:
        await ctx.send("``` text User is already unregistered. ```")
        return