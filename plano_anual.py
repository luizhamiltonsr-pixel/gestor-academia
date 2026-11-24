from models.plano import Plano


class PlanoAnual(Plano):
    """Plano de 12 meses, com 20% de desconto."""

    DESCONTO = 0.20

    def __init__(self):
        super().__init__("Anual", 99.90, 12)

    def valor_total(self):
        # Sobrescreve o método da classe Plano para aplicar o desconto
        return super().valor_total() * (1 - self.DESCONTO)
