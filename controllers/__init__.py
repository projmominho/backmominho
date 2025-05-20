from fastapi import HTTPException


# Processa as exceções e levanta um HTTPException com o status_code e o payload
def handle_error(e):
    print(str(e))
    if e is None:
        raise HTTPException(
            status_code=500, detail={"message": "Erro interno desconhecido"}
        )

    payload = getattr(e, "payload", None)
    if payload is None:
        raise HTTPException(status_code=500, detail={"message": str(e)})

    status_code = payload.get("status_code", 500)
    raise HTTPException(status_code=status_code, detail=payload)
