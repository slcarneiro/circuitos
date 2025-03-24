####################################################################################
# 
#                    PROJETO CIRCUITOS 2 (CONVOLUÇÃO)
#
# AUTORES: Eduardo Piassaroli, Sérgio Luiz
# DATA: 24/03/2025
# ENGENHARIA ELÉTRICA, UFES 
#
####################################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

def analise_circuit(circuit:Circuit, step_time:int, end_time:int):
    # Simulação
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=step_time @ u_us, end_time=end_time @ u_us)

    # Plotando os resultados
    time = np.array(analysis.time) * 1e3  # Convertendo tempo para milissegundos
    voltage_out = np.array(analysis.vout)  # Tensão 

    
    return time, voltage_out

def sinal_quadrado(x):
    return 0 if x < 3 or x > 5 else 2

def sinal_triangular(x):
    return 0 if x < 0 or x > 2 else x

def deslocar_array(arr, deslocamento):
    """
    Desloca o array para a direita (deslocamento positivo) ou para a esquerda (deslocamento negativo),
    preenchendo os novos espaços com zero, sem reintroduzir valores deslocados.
    """
    if deslocamento > 0:
        return np.pad(arr, (deslocamento, 0), mode='constant')[:len(arr)]
    elif deslocamento < 0:
        return np.pad(arr, (0, -deslocamento), mode='constant')[-len(arr):]
    else:
        return arr  # Sem deslocamento

def plot(sinal1:np.ndarray, sinal2:np.ndarray, times:np.ndarray):
    time = len(times)
    if (time != len(sinal1)):
        print("tamanho incorreto!")
        exit(1)
    if (time != len(sinal2)):
        print("tamanho incorreto!")
        exit(1)
    
     # Espelhar o sinal 2 em relação a t=0
    sinal2_espelhado = sinal2[::-1]

    # Cálculo da convolução
    convolucao = signal.convolve(sinal1, sinal2)
    comprimento_convolucao = time

    # Configuração da figura em grid 2x2
    fig, eixos = plt.subplots(2, 2, figsize=(6, 6))

    eixo1, eixo2, eixo3, eixo4 = eixos.flatten()

    eixo1.set_title("h (resposta ao impulso)")
    eixo1.set_xlim(times[0], times[-1])  # Define os limites do eixo X com os valores reais do tempo
    eixo1.set_ylim(-(max(sinal2) + 1), max(sinal1) + 1)   # Define os limites do eixo Y baseado no sinal1
    eixo1.plot(times, sinal1, 'b', lw=2) # Plota sinal1 ao longo de times em azul

    eixo3.set_title("x (entrada arbitrária)")
    eixo3.set_xlim(times[0], times[-1])
    eixo3.set_ylim(-(max(sinal2) + 1), max(sinal2) + 1)
    eixo3.plot(times, sinal2, 'r', lw=2)

    eixo2.set_title("Gráficos deslocados")
    eixo2.set_xlim(times[0], times[-1])
    eixo2.set_ylim(-(max(sinal2) + 1), max(sinal1) + 1)
    eixo2.plot(times, sinal1, 'b', lw=2)
    linha3b, = eixo2.plot([], [], 'r', lw=2)

    eixo4.set_title("Resultado da Convolução")
    eixo4.set_xlim(times[0], times[-1])
    eixo4.set_ylim(-(max(convolucao) + 1), max(convolucao) + 1)
    linha4, = eixo4.plot([], [], 'g', lw=2)

    # Função de inicialização
    def inicializar():
        linha3b.set_data([], [])
        linha4.set_data([], [])
        return linha3b, linha4

    # Função de atualização
    def atualizar(frame):
        deslocado = deslocar_array(sinal2_espelhado, frame-time)
        linha3b.set_data(times, deslocado)
        # linha4.set_data(np.arange(min(frame, time)), convolucao[:min(frame, time)])
        linha4.set_data(times[:min(frame, time)], convolucao[:min(frame, time)])
        return linha3b, linha4

    # Criação da animação
    animacao = animation.FuncAnimation(
        fig, atualizar, frames=comprimento_convolucao, init_func=inicializar, blit=True, interval=1
    )

    plt.tight_layout()
    plt.show()

def main():
    # Definição do circuito RC
    circuit = Circuit("RC Circuit")
        
    # # Circuito RC
    circuit.V(1, "vin", circuit.gnd, f"PULSE(0V 10V 0ms 1us 1us 1000us 100000s)")  # Pulso de 5V    
    circuit.R(1, "vin", "vout", 1 @ u_kOhm)  # Resistor de 1kΩ
    circuit.C(1, "vout", circuit.gnd, 3 @ u_uF)  # Capacitor de 1µF
    
    # # Circuito RL
    # circuit.V(1, "vin", circuit.gnd, f"PULSE(0V 10V 0ms 1us 1us 1000us 100000s)")  # Pulso de 5V
    # circuit.L(1, "vin", "vout", 3 @ u_H)  
    # circuit.R(1, "vout", circuit.gnd, 1 @ u_kOhm)  # Resistor de 1kΩ
    
    # # Circuito RCL série
    # circuit.V(1, "vin", circuit.gnd, f"PULSE(0V 10V 0ms 1us 1us 1000us 100000s)")  # Pulso de 5V    
    # circuit.C(1, "vin", "inter", 3 @ u_uF)  # Capacitor de 1µF
    # circuit.L(1, "inter", "vout", 3 @ u_H)  
    # circuit.R(1, "vout", circuit.gnd, 1 @ u_kOhm)  # Resistor de 1kΩ
    
    # # Circuito RCL paralelo
    # circuit.V(1, "vin", circuit.gnd, f"PULSE(0V 10V 0ms 1us 1us 1000us 100000s)")  # Pulso de 5V    
    # circuit.C(1, "vin", "vout", 3 @ u_uF)  # Capacitor de 1µF
    # circuit.L(1, "vout", circuit.gnd, 3 @ u_H)  
    # circuit.R(1, "vout", circuit.gnd, 1 @ u_kOhm)  # Resistor de 1kΩ
    
    # Geração dos sinais
    # O "impulso" tem duração de 1ms, então recomenda-se pelo menos 10ms para tempo total
    stop_time = 10 # em us
    end_time = 20000 # em us
    times, h = analise_circuit(circuit, stop_time, end_time)
    
    x = np.array([2 if  x < 0.2*len(times) else 0 for x in range(len(times))])
    
    times = times/1000
    plot(h, x, times)
    
if __name__ == "__main__":
    main()