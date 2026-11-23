import number_generator as ng
import stadistic_test as st
import file_loader as fl
import variables_aleatorias as va

#numeros = ng.conguencial_mixto(457,129,17,2053)
generador = ng.congruencial_generator(457,129,17)
#numeros = generador.generate_numbers()
#print("Numeros generados con congruencial: " + str(numeros))
print("Numeros generados con congruencial: " + str(generador.numbers))
print("Numeros generados con congruencial normalizados: " + str(generador.get_normalized_numbers()))
print("Numeros generados con congruencial: " + str(generador.numbers))



'''numeros = ng.congruencial_generator(457,129,17).generate_numbers()
print("Numeros generados con congruencial: " + str(numeros))
numerosNormalizados = ng.congruencial_generator(457,129,17).get_normalized_numbers()
print("Numeros normalizados con congruencial: " + str(numerosNormalizados))
numeros2 = ng.congruencial_mixto_generator(457,129,17,2053).generate_numbers()
print("Numeros generados con congruencial mixto: " + str(numeros2))'''
'''st.media_test(numeros)
st.kolmogorov_smirnoff(numeros)
st.frequency_test(numeros)
st.poker_test(numeros)'''
