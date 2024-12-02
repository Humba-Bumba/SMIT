from datetime import datetime

from fastapi import APIRouter, Depends

from database.postgres import get_session, AsyncSession
from service.common import get_rate, add_rate, delete_rate
from models.rate import Rate

router = APIRouter(prefix='/api/insurance',
                   tags=['Панель пользователя - Раздел Страхование'])


@router.get("/calculate",
            summary="Получить калькуляцию",
            description="Получить калькуляцию",
            response_description="Получить калькуляцию"
            )
def calculate_insurance(cargo_type: str, declared_value: float, date: str, session: AsyncSession = Depends(get_session)):
    rate = get_rate(cargo_type, date, session)
    if not rate:
        return {"error": "Rate not found"}
    return {"insurance_cost": declared_value * rate.rate}


@router.post("/rates/",
             summary="Изменить ставку",
             description="Изменить ставку",
             response_description="Изменить ставку"
             )
def create_rate(cargo: Rate, session: AsyncSession = Depends(get_session)):
    date_obj = datetime.strptime(cargo.date, "%Y-%m-%d").date()

    # Создаём новый объект для записи в базу данных
    cargo_calculation = Rate(date=date_obj, cargo_type=cargo.cargo_type, rate=cargo.rate)

    new_rate = add_rate(cargo.cargo_type, cargo.rate, session)
    return new_rate


@router.delete("/rates/{rate_id}",
               summary="Удалить ставку",
               description="Удалить ставку",
               response_description="Удалить ставку"
               )
def remove_rate(rate_id: int, session: AsyncSession = Depends(get_session)):
    delete_rate(rate_id, session)
    return {"status": "deleted"}
