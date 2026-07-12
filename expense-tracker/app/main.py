from fastapi import FastAPI

app = FastAPI(
    title="Expense Tracker API",
    description="개인 지출 관리 학습 프로젝트",
    version="0.0.1",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Expense Tracker API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
