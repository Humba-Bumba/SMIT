from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from database.postgres import get_session, AsyncSession
from service import common

router = APIRouter(prefix='/api/human',
                   tags=['Панель пользователя'])


@router.get("/getPercent",
            summary="Получить процент",
            description="Получение процента",
            response_description="Полученный процент"
            )
async def get_percent(audience1: str, audience2: str, session: AsyncSession = Depends(get_session)):
    common.valid_request(audience1)
    common.valid_request(audience2)

    modified_text1 = common.add_quotes(audience1)
    modified_text2 = common.add_quotes(audience2)

    try:
        percent = await common.custom_query(modified_text1, modified_text2, session)

        return {"percent": percent}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"SQL Error: {str(e)}")

