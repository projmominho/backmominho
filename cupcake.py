from fastapi import APIRouter
from db import get_rows

router = APIRouter()


# seleciona todos os bolinhos
@router.get("/cupcakes")
def select_cupcakes():
    query = """
        SELECT id, nome, descricao, preco, disponibilidade, ingredientes, peso, dimensoes, informacoesNutricionais
        FROM Cupcake
    """
    rows = get_rows(query)

    cupcakes = []
    for row in rows:
        cupcakes.append(
            {
                "id": row[0],
                "nome": row[1],
                "descricao": row[2],
                "preco": float(row[3]),
                "disponivel": row[4],
                "ingredientes": row[5],
                "peso": row[6],
                "dimensoes": row[7],
                "informacoesNutricionais": row[8],
            }
        )

    return cupcakes
