from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app=FastAPI()

class TodoItem(BaseModel):
    id: uuid4
    title: str
    description: str


# Hello word Get
@app.get('/')
def read():
    return {"Name": "Hello, World!"}


# Hello Greeting Post
@app.post('/greet')
def greet(name: str, Pass: str):
    return {"Greeting": "Hello, "+ name}

todo_db=[]


# Add Todo Items into the list
@app.post('/todo', response_model=TodoItem)
def TodoItems(item: TodoItem):
    todo_db.append(item)
    return item


# get All Todo Items
@app.get('/todo', response_model=List[TodoItem])
def getAllTodoItems():
    return todo_db


# Get a specific TodoIte by Id
@app.get('/todo/{id}', response_model=TodoItem)
def getTodoItemById(id: str):
    for item in todo_db:
        if str(item.id)==id:
            return item
    
    return {"Error": "Item not Found"}


# Search TodoItems by title
@app.get('/todo/search/{title}', response_model=List[TodoItem])
def searchTodoItemByTitle(title: str):
    search_Items=[]
    for item in todo_db:
        if title.lower() in item.title.lower():
            search_Items.append(item)
    if len(search_Items)>0:
        return search_Items
    
    return {"Error": "Item Not Found Try an other Title"}


# Delete a specific TodoItem by Id
@app.delete('/todo/{id}', response_model=TodoItem)
def DeleteTodoItemById(id: str):
    for index, item in enumerate(todo_db):
        if str(item.id)==id:
            todo_db.pop(index)
            return {"Message": "Item Deleted Successfully"}
    
    return {"Error": "Item not Found"}


class UpdateTodoItem(BaseModel):
    description: str


# Update a Specific TodoItem by Id
@app.put('/todo/{id}', response_model=TodoItem)
def UpdayeTodoItemById(id: str, updated_item: UpdateTodoItem):
    for index, item in enumerate(todo_db):
        if(str(item.id)==id):
            todo_db[index].description=updated_item.description
            return todo_db[index]

    return {"Error": "Item not Found"}



if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
