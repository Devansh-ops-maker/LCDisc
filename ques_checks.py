import aiohttp
import random
from datetime import datetime

URL = "https://leetcode.com/graphql"


async def get_problem(difficulty):
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        questions: data {
          title
          titleSlug
          difficulty
          isPaidOnly
        }
      }
    }
    """

    variables = {
        "categorySlug": "",
        "limit": 5000,
        "skip": 0,
        "filters": {}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json={"query": query, "variables": variables}) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()

    if "errors" in data:
        return None

    questions = data["data"]["problemsetQuestionList"]["questions"]

    pool = [
        q for q in questions
        if q["difficulty"] == difficulty and not q["isPaidOnly"]
    ]

    if not pool:
        return None

    problem = random.choice(pool)

    return {
        "title": problem["title"],
        "slug": problem["titleSlug"],
        "url": f"https://leetcode.com/problems/{problem['titleSlug']}/"
    }


async def get_problem_by_topic(topic, difficulty=None):
    query = """
    query getProblemsByTopic($topic: String!) {
      problemsetQuestionList: questionList(
        categorySlug: ""
        limit: 5000
        filters: {
          tags: [$topic]
        }
      ) {
        questions: data {
          title
          titleSlug
          difficulty
          isPaidOnly
        }
      }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "topic": topic
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()

    if "errors" in data:
        return None

    questions = data["data"]["problemsetQuestionList"]["questions"]

    if difficulty is None:
        pool = [
            q for q in questions
            if not q["isPaidOnly"]
        ]
    else:
        pool = [
            q for q in questions
            if q["difficulty"] == difficulty and not q["isPaidOnly"]
        ]

    if not pool:
        return None

    problem = random.choice(pool)

    return {
        "title": problem["title"],
        "slug": problem["titleSlug"],
        "url": f"https://leetcode.com/problems/{problem['titleSlug']}/"
    }
async def get_recent_submissions(username, limit=5):
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            title
            titleSlug
            timestamp
        }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "username": username,
            "limit": limit
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:

            if resp.status != 200:
                return None

            data = await resp.json()

    if "errors" in data:
        return None

    return data["data"]["recentAcSubmissionList"]


async def check_question(username, problem_link):

    submissions = await get_recent_submissions(username)

    if submissions is None:
        return None

    slug = problem_link.rstrip("/").split("/")[-1]

    for submission in submissions:
        if submission["titleSlug"] == slug:
            return int(submission["timestamp"])

    return None


async def get_problem_by_topic(topic, difficulty=None):
    query = """
    query getProblemsByTopic($topic: String!) {
      problemsetQuestionList(
        categorySlug: ""
        limit: 5000
        filters: {
          tags: [$topic]
        }
      ) {
        questions {
          title
          titleSlug
          difficulty
          isPaidOnly
        }
      }
    }
    """

    payload = {
        "query": query,
        "variables": {
            "topic": topic
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=payload) as resp:
            if resp.status != 200:
                return None

            data = await resp.json()

    if "errors" in data:
        return None

    questions = data["data"]["problemsetQuestionList"]["questions"]

    if difficulty is None:
        pool = [
            q for q in questions
            if not q["isPaidOnly"]
        ]
    else:
        pool = [
            q for q in questions
            if q["difficulty"] == difficulty and not q["isPaidOnly"]
        ]

    if not pool:
        return None

    problem = random.choice(pool)

    return {
        "title": problem["title"],
        "slug": problem["titleSlug"],
        "url": f"https://leetcode.com/problems/{problem['titleSlug']}/"
    }