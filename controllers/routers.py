from .vitrine import router_vitrine
from .pedido import router_pedido
from .pagamento import router_pagamento
from .admin import router_admin

routers = [router_vitrine, router_pedido, router_pagamento, router_admin]
