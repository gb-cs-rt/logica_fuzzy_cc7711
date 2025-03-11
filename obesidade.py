#pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 8, 1), 'comer')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 10, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
comer.automf(names=['pouco','razoavel','bastante'],)

# atribuicao sem o automf
peso['peso leve'] = fuzz.trapmf(peso.universe, [-1, 0, 4, 6])
peso['peso medio'] = fuzz.trapmf(peso.universe, [4, 6, 8, 10])
peso['pesado'] = fuzz.trapmf(peso.universe, [8, 10, 12, 14])

#Visualizando as variáveis
comer.view()
peso.view()

#Criando as regras
regra_1 = ctrl.Rule(comer['bastante'], peso['pesado'])
regra_2 = ctrl.Rule(comer['razoavel'], peso['peso medio'])
regra_3 = ctrl.Rule(comer['pouco'], peso['peso leve'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])

#Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

notaPeso = int(input('Comer: '))
CalculoPeso.input['comer'] = notaPeso
CalculoPeso.compute()

valorPeso = CalculoPeso.output['peso']

print("\n Comer %d \nPeso %5.2f" % (notaPeso,valorPeso))


comer.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

plt.show()