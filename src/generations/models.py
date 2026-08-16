from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from core.database import Base


class GenerationJobModel(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer,primary_key=True,autoincrement=True)
    request_id = Column(String,nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    prompt = Column(Text,nullable=False)
    status = Column(String,nullable=False,default="IN_QUEUE")
    cost = Column(Float,nullable=False)
    is_refunded = Column(Boolean,nullable=False,default=False)
    result_url = Column(String,nullable=True)