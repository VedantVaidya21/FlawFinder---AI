from fastapi import FastAPI
from routers import auth, upload, analyze, dashboard, fix_plan, report
from db.session import engine, Base
import uvicorn

app = FastAPI(title="FlawFinder AI", version="1.0.0")

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(fix_plan.router, prefix="/fix-plan", tags=["Fix Plan"])
app.include_router(report.router, prefix="/report", tags=["Report"])

# Create tables (for demo, use migrations in prod)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
