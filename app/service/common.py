from fastapi import Depends

from database.postgres import get_session, AsyncSession
from models.rate import Rate


async def get_rate(cargo_type: str, date: str, session: AsyncSession = Depends(get_session)):
    return session.query(Rate).filter(Rate.cargo_type == cargo_type, Rate.effective_date <= date).first()


async def add_rate(cargo_type: str, rate: float, session: AsyncSession = Depends(get_session)):
    db_rate = Rate(cargo_type=cargo_type, rate=rate)
    session.add(db_rate)
    session.commit()
    session.refresh(db_rate)
    return db_rate


async def delete_rate(rate_id: int, session: AsyncSession = Depends(get_session)):
    session.query(Rate).filter(Rate.id == rate_id).delete()
    session.commit()
