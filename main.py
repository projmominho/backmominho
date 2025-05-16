from fastapi import FastAPI

app = FastAPI()


@app.get("/cupcake")
def get_cupcake():
    return {"id": 1, "nome": "Red Velvet", "preco": 12.50, "disponivel": True}
