from fastapi import FastAPI

app = FastAPI() # 创建 api 对象

@app.get('/') # 根路由
async def root():
    return {'message':'Hello, FastAPI'}