INVESTIGATION_PROMPT = """
You are a software investigation expert.

Issue:
{issue}

Investigation Plan:
{plan}

Based on the investigation plan, identify the important keywords
that should be searched in the repository.

Return only a comma-separated list.

Example:
login, authenticate, jwt
"""