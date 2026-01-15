from __future__ import annotations
import random

# ----------------------------------------------------------------------------

# Ganha de, que ganha de, que ganha de...
# Pedra → Papel → Tesoura → Pedra

# Pedra–Papel–Tesoura com frases canônicas (sem fórmula, sem aritmética modular)

# Mapa explícito de vitórias com frases
REGRAS = {
    ("Tesoura", "Papel"): "Tesoura corta Papel",
    ("Papel", "Pedra"):   "Papel cobre Pedra",
    ("Pedra", "Tesoura"): "Pedra quebra Tesoura",
}

def jogo_ppt_frases(a: str, b: str) -> str:
    """
    Retorna o resultado usando regras explícitas e frases canônicas.
    """
    if a == b:
        return "Empate"

    if (a, b) in REGRAS:
        return f"Jogador A vence: {REGRAS[(a, b)]}"

    if (b, a) in REGRAS:
        return f"Jogador B vence: {REGRAS[(b, a)]}"

    validas = {"Pedra", "Papel", "Tesoura"}
    if a not in validas or b not in validas:
        raise ValueError(f"Jogadas válidas: {', '.join(validas)}")

    # Este ponto nunca deve ser alcançado se as regras estiverem corretas
    raise RuntimeError("Estado inválido do jogo")


# Exemplos:
# print(jogo_ppt_frases("Tesoura", "Papel"))
print(jogo_ppt_frases("Pedra", "Papel"))
# print(jogo_ppt_frases("Pedra", "Pedra"))

# ----------------------------------------------------------------------------

# Codificação cíclica: Pedra(0) -> Papel(1) -> Tesoura(2) -> Pedra(0)
_MAP = {"Pedra": 0, "Papel": 1, "Tesoura": 2}
_REV = {v: k for k, v in _MAP.items()}

def Jogo(mov_jogador_A: str, mov_jogador_B: str) -> str:
    """
    Retorna: "Jogador A", "Jogador B" ou "Empate".
    Entradas válidas: "Pedra", "Papel", "Tesoura".
    """
    try:
        a = _MAP[mov_jogador_A]
        b = _MAP[mov_jogador_B]
    except KeyError:
        raise ValueError('Jogadas válidas: "Pedra", "Papel", "Tesoura".')

    r = (a - b) % 3
    if r == 0:
        return "Empate"
    return "Jogador A" if r == 1 else "Jogador B"


def JogoContraComputador(movimento_alice: str) -> tuple[str, str]:
    """
    Alice é o Jogador A e o computador é o Jogador B (aleatório).
    Retorna (resultado, movimento_computador).
    """
    mov_pc = _REV[random.randrange(3)]
    return Jogo(movimento_alice, mov_pc), mov_pc


# Exemplos:
# print(Jogo("Pedra", "Tesoura"))   # Jogador A
print(Jogo("Tesoura", "Pedra"))   # Jogador B
# resultado, pc = JogoContraComputador("Papel")
# print("PC:", pc, "=>", resultado)

# Porque essa fórmula funciona...
'''
| A | B | a-b | (a-b) % 3 | Resultado |
| - | - | --- | --------- | --------- |
| 0 | 0 | 0   | 0         | Empate    |
| 1 | 1 | 0   | 0         | Empate    |
| 2 | 2 | 0   | 0         | Empate    |
| 0 | 2 | -2  | 1         | A ganha   |
| 1 | 0 | 1   | 1         | A ganha   |
| 2 | 1 | 1   | 1         | A ganha   |
| 2 | 0 | 2   | 2         | B ganha   |
| 0 | 1 | -1  | 2         | B ganha   |
| 1 | 2 | -1  | 2         | B ganha   |

           a == b ?
              |
         +----Sim----+ → Empate
         |
        Não
         |
   r = (a - b) % 3
         |
      r == 1 ?
     /        \
   Sim        Não
   |           |
Jogador A   Jogador B

'''

# ----------------------------------------------------------------------------

# Codificação cíclica (ordem ímpar, consistente):
# Cada jogada ganha das 2 anteriores no ciclo.
MAP = {
    "Pedra":   0,
    "Spock":   1,
    "Papel":   2,
    "Lagarto": 3,
    "Tesoura": 4,
}
REV = {v: k for k, v in MAP.items()}

def jogo_pplsp(a: str, b: str) -> str:
    """
    Retorna: "Empate", "Jogador A" ou "Jogador B"
    Usando a fórmula modular para n=5.
    """
    try:
        ia, ib = MAP[a], MAP[b]
    except KeyError:
        validas = ", ".join(MAP.keys())
        raise ValueError(f"Jogadas válidas: {validas}")

    r = (ia - ib) % 5

    if r == 0:
        return "Empate"
    # Para n ímpar=5: A ganha se 1 <= r <= (n-1)//2 == 2
    return "Jogador A" if 1 <= r <= 2 else "Jogador B"


# Exemplos rápidos:
# print(jogo_pplsp("Spock", "Tesoura"))   # Jogador A
# print(jogo_pplsp("Lagarto", "Pedra"))   # Jogador B
# print(jogo_pplsp("Papel", "Papel"))     # Empate

