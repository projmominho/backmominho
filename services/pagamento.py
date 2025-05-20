from services.service_error import ServiceError
from services.pedido import pedido_service
from models.pedido import Pedido
from mytwilio import whats_pedido_atualizado
import re
import asyncio


class PagamentoService:
    # rotinas finais após pagamento concluído
    async def finalizar_pagamento(
        self, session, pedido_id: int, valor_pago: float, tipo_pagamento: str
    ):
        await pedido_service.atualizar_valor_pago(session, pedido_id, valor_pago)

        pedido = await session.get(Pedido, pedido_id)
        mensagem = f"MOMINHO: seu pedido #{pedido_id} foi pago!"

        whats_pedido_atualizado(
            to=pedido.telefone, codigo_pedido=f"{pedido_id}?telefone={pedido.telefone}"
        )

        status_msg = (
            f"Pagamento realizado no valor de R${valor_pago:.2f} via {tipo_pagamento}"
        )
        await pedido_service.atualizar_status(session, pedido_id, status_msg)

        return True

    # faz o pagamento por cartão de crédito
    async def pagamento_cartao(self, session, payload):
        pedido_id = int(payload.get("id"))
        numero = re.sub(r"\D", "", payload.get("numero", ""))
        validade = re.sub(r"\D", "", payload.get("validade", ""))
        cvv = re.sub(r"\D", "", payload.get("cvv", ""))

        # Número do cartão: 16 dígitos
        if len(numero) != 16:
            raise ServiceError(
                payload={
                    "message": "Número do cartão deve ter 16 dígitos.",
                    "status_code": 400,
                }
            )

        # Validade: 4 dígitos (MMYY)
        if len(validade) < 4:
            raise ServiceError(
                payload={
                    "message": "Validade deve ter 4 dígitos com mês e ano (ex: 0525).",
                    "status_code": 400,
                }
            )

        mes = int(validade[:2])
        ano = int(validade[2:4])
        ano_atual = int(str(__import__("datetime").datetime.now().year)[-2:])
        ultimo_ano = ano_atual - 20  # aceita validade no máximo 20 anos atrás

        if mes < 1 or mes > 12:
            raise ServiceError(
                payload={
                    "message": "Mês inválido na validade (use MM/AA, mês de 01 a 12).",
                    "status_code": 400,
                }
            )

        if ano < ultimo_ano:
            raise ServiceError(
                payload={
                    "message": f"Ano inválido na validade. O cartão não pode ser mais velho que 20{str(ultimo_ano).zfill(2)}.",
                    "status_code": 400,
                }
            )

        # CVV: 3 ou 4 dígitos
        if len(cvv) < 3 or len(cvv) > 4:
            raise ServiceError(
                payload={"message": "CVV deve ter 3 ou 4 dígitos.", "status_code": 400}
            )

        await asyncio.sleep(3)

        # Teste específico: cartão fake 9999
        if numero == "9999999999999999":
            raise ServiceError(
                payload={
                    "message": "Saldo insuficiente para concluir a compra.",
                    "status_code": 402,
                }
            )

        itens, valor_total = await pedido_service.listar_itens_e_total(
            session, pedido_id
        )

        await self.finalizar_pagamento(
            session, pedido_id, valor_total, "cartão de crédito"
        )

        return {"message": "Pagamento confirmado!", "pedido_id": pedido_id}

    # faz o pagamento por pix
    async def pagamento_pix(self, session, payload):
        pedido_id = int(payload.get("id"))
        itens, valor_total = await pedido_service.listar_itens_e_total(
            session, pedido_id
        )

        await self.finalizar_pagamento(session, pedido_id, valor_total, "PIX")

        await asyncio.sleep(1)

        return {"message": "Pagamento confirmado!", "pedido_id": payload.get("id")}


pagamento_service = PagamentoService()
