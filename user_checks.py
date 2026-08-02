import aiohttp

URL = "https://leetcode.com/graphql"


async def user_exists(username):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
      }
    }
    """

    variables = {"username": username}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        ) as response:

            if response.status != 200:
                return False

            data = await response.json()
            if data.get("errors") or "data" not in data:
                return False

            return data["data"]["matchedUser"] is not None


async def check_readme(username):
    query = """
    query getProfile($username: String!) {
      matchedUser(username: $username) {
        profile {
          aboutMe
        }
      }
    }
    """

    variables = {"username": username}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"},
        ) as response:

            if response.status != 200:
                return None

            data = await response.json()
            if data.get("errors") or "data" not in data:
                return None

            matched_user = data["data"]["matchedUser"]
            if matched_user is None:
                return None

            return matched_user["profile"]["aboutMe"]