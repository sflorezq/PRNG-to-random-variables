import number_generator as ng
import stadistic_test as st
import file_loader as fl
import variables_aleatorias as va

numeros = ng.conguencial_mixto(457,129,17,2053)
st.media_test(numeros)
st.kolmogorov_smirnoff(numeros)
st.frequency_test(numeros)
st.poker_test(numeros)
