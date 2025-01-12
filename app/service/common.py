import re

from fastapi import Depends, HTTPException
from sqlalchemy.sql import text

from database.postgres import get_session, AsyncSession


DISALLOWED_PATTERNS = [
    r"(?i)\b(SELECT|DROP|DELETE|INSERT|UPDATE|UNION|ALTER|CREATE|GRANT|EXEC)\b",
    r"--",
    r"\/\*",
    r"\*\/",
    r"'",
    r";",
]


def valid_request(request: str) -> None:
    """
    Validates the request string to ensure it doesn't contain any potentially dangerous patterns

    :param request: Condition to validate
    :raises HTTPException: If any dangerous patterns are found in the request
    """
    for pattern in DISALLOWED_PATTERNS:
        if re.search(pattern, request):
            raise HTTPException(
                status_code=400,
                detail=f"Detected potentially dangerous operation in condition: {request}"
            )


def add_quotes(user_request: str) -> str:
    """
    Adding quotes for correct work with the database

    :param user_request: The SQL-like condition to modify
    :return: Correct sql request
    """
    keywords = ['Date', 'respondent', 'Sex', 'Age', 'Weight']
    for word in keywords:
        user_request = re.sub(rf'\b{word}\b', f'"{word}"', user_request)
    return user_request


async def custom_query(modified_text1: str, modified_text2: str, session: AsyncSession = Depends(get_session)) -> float:
    """
    Executes two SQL queries with the provided conditions and calculates the percentage of the second audience
    in the first

    :param modified_text1: The SQL condition for the first audience
    :param modified_text2: The SQL condition for the second audience
    :param session: The database session
    :return: The calculated percentage of the second audience in the first
    """
    query1 = text(f"""
                SELECT respondent, AVG("Weight") as avg_weight
                FROM human
                WHERE {modified_text1}
                GROUP BY respondent
            """)

    query2 = text(f"""
                SELECT respondent, AVG("Weight") as avg_weight
                FROM human
                WHERE {modified_text2}
                GROUP BY respondent
           """)
    try:
        result1 = await session.execute(query1)
        result2 = await session.execute(query2)

        percent = percentage_entry(result1, result2)
        return percent

    except Exception as e:
        raise e


def percentage_entry(data1, data2) -> float:
    """
    Calculates the percentage of the second audience entering the first, based on average weight

    :param data1: First audience result
    :param data2: Second audience result
    :return: The percentage of the second audience in the first based on average weight
    """
    audience1_data = {row[0]: row[1] for row in data1.fetchall()}
    audience2_data = {row[0]: row[1] for row in data2.fetchall()}

    common_respondents = set(audience1_data.keys()).intersection(set(audience2_data.keys()))

    if not common_respondents:
        return 0.0

    if audience1_data == audience2_data:
        return 1.0

    sum_weight_audience2 = sum(audience2_data[resp] for resp in common_respondents)

    total_weight_audience1 = sum(audience1_data.values())

    percent = sum_weight_audience2 / total_weight_audience1
    return percent
