from fastapi import FastAPI

app = FastAPI()

# first get method
# to run use uvicorn main:app --reload
# or try this: python -m uvicorn main:app --reload
@app.get("/")
def read_root():
    return {"Hello": "World"}