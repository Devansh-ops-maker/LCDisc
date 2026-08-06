from ques_checks import get_problem


async def recommend(ctx, difficulty: str):

    difficulty = difficulty.lower()

    if difficulty == "easy" or difficulty == "medium" or difficulty == "hard":
        if difficulty == "easy":
            ques = await get_problem("Easy")
        elif difficulty == "medium":
            ques = await get_problem("Medium")
        else:
            ques = await get_problem("Hard")

        if ques is None:
            await ctx.send("``` text Couldn't fetch a problem right now — try again in a bit.```")
            return

        await ctx.send(
            f"**{ques['title']}**\n{ques['url']}"
        )
        return
    else:
        await ctx.send("``` text Invalid difficulty level entered.```")
        return