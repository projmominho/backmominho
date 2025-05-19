class ServiceError(Exception):
    # Exceção customizada para erros de serviço com payload que inclui mensagem e código de status
    def __init__(self, payload=None):
        self.payload = payload or {}
        self.payload["message"] = self.payload.get("message", "Erro de serviço")
        super().__init__(self.payload["message"])
