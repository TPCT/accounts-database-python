from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Controllers.AccountsController import AccountsController
import uvicorn

origins = ['*']
methods = ['*']
headers = ['*']

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=methods, allow_headers=headers)
app.include_router(AccountsController.Router)

if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        reload_dirs=['./Models', './Controllers', './Requests']
    )