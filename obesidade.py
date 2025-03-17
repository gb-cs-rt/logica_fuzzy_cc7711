#pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 12, 1), 'comer') # 1000 kcal
tempoAtvFisica = ctrl.Antecedent(np.arange(0, 240, 1), 'tempoAtvFisica') # minutos

# Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 14, 1), 'peso')

# Funções de pertinência

# Tempo de Atividade Física
tipo_atv_fisica = "triangular"

if tipo_atv_fisica == "triangular":
    tempoAtvFisica.automf(names=['pouco tempo', 'tempo medio', 'muito tempo'])
elif tipo_atv_fisica == "trapezoidal":
    tempoAtvFisica['pouco tempo'] = fuzz.trapmf(tempoAtvFisica.universe, [0, 0, 30, 60])
    tempoAtvFisica['tempo medio'] = fuzz.trapmf(tempoAtvFisica.universe, [30, 60, 120, 150])
    tempoAtvFisica['muito tempo'] = fuzz.trapmf(tempoAtvFisica.universe, [120, 150, 240, 240])
elif tipo_atv_fisica == "gaussiana":
    tempoAtvFisica['pouco tempo'] = fuzz.gaussmf(tempoAtvFisica.universe, 0, 20)
    tempoAtvFisica['tempo medio'] = fuzz.gaussmf(tempoAtvFisica.universe, 90, 20)
    tempoAtvFisica['muito tempo'] = fuzz.gaussmf(tempoAtvFisica.universe, 240, 20)

# Comer
tipo_comer = "trapezoidal"

if tipo_comer == "triangular":
    comer.automf(names=['pouco', 'razoavel', 'bastante'])
elif tipo_comer == "trapezoidal":
    comer['pouco'] = fuzz.trapmf(comer.universe, [0, 0, 2, 4])
    comer['razoavel'] = fuzz.trapmf(comer.universe, [2, 4, 12, 12])
    comer['bastante'] = fuzz.trapmf(comer.universe, [4, 6, 12, 12])
elif tipo_comer == "gaussiana":
    comer['pouco'] = fuzz.gaussmf(comer.universe, 0, 2)
    comer['razoavel'] = fuzz.gaussmf(comer.universe, 6, 2)
    comer['bastante'] = fuzz.gaussmf(comer.universe, 12, 2)

# Peso
tipo_peso = "trapezoidal"

if tipo_peso == "triangular":
    peso.automf(names=['peso leve', 'peso medio', 'pesado'])
elif tipo_peso == "trapezoidal":
    peso['peso leve'] = fuzz.trapmf(peso.universe, [0, 0, 4, 6])
    peso['peso medio'] = fuzz.trapmf(peso.universe, [4, 6, 8, 10])
    peso['pesado'] = fuzz.trapmf(peso.universe, [8, 10, 14, 14])
elif tipo_peso == "gaussiana":
    peso['peso leve'] = fuzz.gaussmf(peso.universe, 0, 2)
    peso['peso medio'] = fuzz.gaussmf(peso.universe, 6, 2)
    peso['pesado'] = fuzz.gaussmf(peso.universe, 12, 2)

#Visualizando as variáveis
comer.view()
tempoAtvFisica.view()
peso.view()

# Usar tempo de atividade física
usar_tempo_atv_fisica = True

if not usar_tempo_atv_fisica:

    # Criando as regras (somente uma variável de entrada)
    regra_1_1 = ctrl.Rule(comer['bastante'], peso['pesado'])
    regra_1_2 = ctrl.Rule(comer['razoavel'], peso['peso medio'])
    regra_1_3 = ctrl.Rule(comer['pouco'], peso['peso leve'])
    controlador = ctrl.ControlSystem([regra_1_1, regra_1_2, regra_1_3])

else:

    # Criando as regras (duas variáveis de entrada)
    regra_2_1 = ctrl.Rule(comer['bastante'] | tempoAtvFisica['pouco tempo'], peso['pesado'])
    regra_2_2 = ctrl.Rule(comer['razoavel'] & tempoAtvFisica['tempo medio'], peso['peso medio'])
    regra_2_3 = ctrl.Rule(comer['pouco'] & tempoAtvFisica['muito tempo'], peso['peso leve'])
    regra_2_4 = ctrl.Rule(comer['pouco'] & tempoAtvFisica['pouco tempo'], peso['peso leve'])
    regra_2_5 = ctrl.Rule(comer['bastante'] & tempoAtvFisica['muito tempo'], peso['peso medio'])
    controlador = ctrl.ControlSystem([regra_2_1, regra_2_2, regra_2_3, regra_2_4, regra_2_5])

#Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

notaPeso = int(input('Comer: '))
CalculoPeso.input['comer'] = notaPeso

if usar_tempo_atv_fisica:
    notaTempoAtvFisica = int(input('Tempo de Atividade Física: '))
    CalculoPeso.input['tempoAtvFisica'] = notaTempoAtvFisica

CalculoPeso.compute()

valorPeso = CalculoPeso.output['peso']

if not usar_tempo_atv_fisica:
    print("\nComer: %d \nPeso: %5.2f\n" % (notaPeso, valorPeso))
else:
    print("\nComer: %d\nTempo de Atividade Física: %d\nPeso: %5.2f \n" % (notaPeso, notaTempoAtvFisica, valorPeso))


comer.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

if usar_tempo_atv_fisica:
    tempoAtvFisica.view(sim=CalculoPeso)

plt.show()