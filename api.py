from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controllers.AccountsController import AccountsController
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from Core.Config import limiter
import uvicorn

origins = ['*']
methods = ['*']
headers = ['*']

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=methods, allow_headers=headers)
app.include_router(AccountsController.Router)

if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        host='127.0.0.1',
        port=8080,
        workers=5,
        limit_max_requests=500,
        limit_concurrency=500,
        reload=True
    )