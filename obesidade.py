#pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 8, 1), 'comer')
tempoAtvFisica = ctrl.Antecedent(np.arange(0, 8, 1), 'tempoAtvFisica')

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 10, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
comer.automf(names=['pouco','razoavel','bastante'],)
tempoAtvFisica.automf(names=['pouco tempo', 'tempo medio', 'muito tempo'])

# atribuicao sem o automf
peso['peso leve'] = fuzz.trapmf(peso.universe, [-1, 0, 4, 6])
peso['peso medio'] = fuzz.trapmf(peso.universe, [4, 6, 8, 10])
peso['pesado'] = fuzz.trapmf(peso.universe, [8, 10, 12, 14])

#Visualizando as variáveis
comer.view()
tempoAtvFisica.view()
peso.view()

#Criando as regras
regra_1 = ctrl.Rule(comer['bastante'] | tempoAtvFisica['pouco tempo'], peso['pesado'])
regra_2 = ctrl.Rule(comer['razoavel'] & tempoAtvFisica['tempo medio'], peso['peso medio'])
regra_3 = ctrl.Rule(comer['pouco'] & tempoAtvFisica['muito tempo'], peso['peso leve'])
regra_4 = ctrl.Rule(comer['pouco'] & tempoAtvFisica['pouco tempo'], peso['peso leve'])
regra_5 = ctrl.Rule(comer['bastante'] & tempoAtvFisica['muito tempo'], peso['pesado'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])

#Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

notaPeso = int(input('Comer: '))
notaTempoAtvFisica = int(input('Tempo de Atividade Física: '))
CalculoPeso.input['comer'] = notaPeso
CalculoPeso.input['tempoAtvFisica'] = notaTempoAtvFisica
CalculoPeso.compute()

valorPeso = CalculoPeso.output['peso']

print("\n Comer %d \nPeso %5.2f \n Tempo de Atividade Física %d \n" % (notaPeso, valorPeso, notaTempoAtvFisica))


comer.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

plt.show()