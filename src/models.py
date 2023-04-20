from pydantic import BaseModel, Field


class Exam(BaseModel):

    class Member(BaseModel):
        id: str = Field(min_length=1)

    class Request(BaseModel):
        count: int = Field(ge=1, le=999)
        interval: float = Field(ge=0, le=999)
        submit_interval: float = Field(ge=0, le=999)
        answer_time: float = Field(ge=0, le=999)
        consistent_time: bool
        correct_rate: float = Field(ge=0, le=1)

    class NormalDistribution(BaseModel):
        enabled: bool
        answer_time_scale: float = Field(ge=0.01, le=999)
        correct_rate_scale: float = Field(ge=0.01, le=999)

    class Cookies(BaseModel):
        session: str = Field(min_length=1)

    member: Member
    request: Request
    normal_distribution: NormalDistribution
    cookies: Cookies
