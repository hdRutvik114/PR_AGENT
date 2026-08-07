PLANNER_PROMPT = """
You are an expert software engineer.

Your task is to create an investigation plan for the given GitHub issue.

Issue:
{issue}

Repository:
{repository}

Generate a concise investigation plan.

Return only the investigation steps.
"""