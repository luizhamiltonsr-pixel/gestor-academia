from models.plano import Plano


class PlanoMensal(Plano):
    """Plano de 1 mês, sem desconto."""

    def __init__(self):
        super().__init__("Mensal", 99.90, 1)
