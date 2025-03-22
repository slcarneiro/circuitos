import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

# Definição dos sinais

def sinal_quadrado(x):
    """
    Retorna um pulso quadrado com amplitude 2 no intervalo de x entre 3 e 5.
    Fora desse intervalo, retorna 0.
    """
    return 0 if x < 3 or x > 5 else 2


def sinal_triangular(x):
    """
    Retorna um pulso triangular crescente de 0 a 2.
    Fora desse intervalo, retorna 0.
    """
    return 0 if x < 0 or x > 2 else x

# Geração dos sinais
sinal1 = np.array([sinal_quadrado(x / 100) for x in range(1000)])  # Pulso quadrado
sinal2 = np.array([sinal_triangular(x / 100) for x in range(200)])  # Pulso triangular

# Cálculo da convolução
convolucao = signal.convolve(sinal1, sinal2)  # Convolução total
comprimento_convolucao = len(convolucao)

# Configuração da figura e dos subgráficos
fig, eixos = plt.subplots(3, 1, figsize=(8, 8))

eixo1, eixo2, eixo3 = eixos  # Atribuindo os subgráficos

eixo1.set_title("Sinal 1 (Pulso Quadrado)")
eixo1.set_xlim(0, len(sinal1))
eixo1.set_ylim(0, max(sinal1) + 1)
linha1, = eixo1.plot([], [], 'b', lw=2)

eixo2.set_title("Sinal 2 (Pulso Triangular)")
eixo2.set_xlim(0, len(sinal2))
eixo2.set_ylim(0, max(sinal2) + 1)
linha2, = eixo2.plot([], [], 'r', lw=2)

eixo3.set_title("Convolução")
eixo3.set_xlim(0, comprimento_convolucao)
eixo3.set_ylim(0, max(convolucao) + 1)
linha3, = eixo3.plot([], [], 'g', lw=2)

# Função de inicialização
def inicializar():
    """Limpa os dados das linhas antes da animação começar."""
    linha1.set_data([], [])
    linha2.set_data([], [])
    linha3.set_data([], [])
    return linha1, linha2, linha3

# Função de atualização da animação
def atualizar(frame):
    """
    Atualiza os gráficos dinamicamente com base no frame atual.
    """
    # Atualiza os primeiros dois sinais
    linha1.set_data(np.arange(len(sinal1[:frame])), sinal1[:frame])
    linha2.set_data(np.arange(len(sinal2[:frame])), sinal2[:frame])

    # Atualiza o resultado da convolução dinamicamente
    linha3.set_data(np.arange(frame), convolucao[:frame])

    return linha1, linha2, linha3

# Criação da animação
animacao = animation.FuncAnimation(
    fig, atualizar, frames=comprimento_convolucao, init_func=inicializar, blit=True, interval=1
)

plt.tight_layout()
plt.show()
