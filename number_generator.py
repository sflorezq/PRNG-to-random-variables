def conguencial_mixto(seed,multiplicative,additive,module):
    numbers = []
    first_number = (multiplicative*seed+additive)%module
    actual_number = first_number
    numbers.append(actual_number)
    while True:
        actual_number = (multiplicative*actual_number+additive)%module
        if(actual_number == first_number):
            break
        numbers.append(actual_number)
    numbers = get_normalized_numbers(numbers,module)
    return numbers

def conguencial_multiplicativo(seed,multiplicative,module):
    numbers = []
    first_number = (multiplicative*seed)%module
    actual_number = first_number
    numbers.append(actual_number)
    while True:
        actual_number= (multiplicative*actual_number)%module
        if(actual_number == first_number):
            break
        numbers.append(actual_number)
    numbers = get_normalized_numbers(numbers,module)
    return numbers

def congruencial_cuadratico(seed,a,b,c,module):
    numbers = []
    first_number = (a*(seed**2)+b*seed+c)%module
    actual_number = first_number
    numbers.append(actual_number)
    while True:
        actual_number= (a*(actual_number**2)+b*actual_number+c)%module
        if(actual_number == first_number):
            break
        numbers.append(actual_number)
    numbers = get_normalized_numbers(numbers,module)
    return numbers

def aditivo(parameters, k,m):
    numbers = parameters
    for i in range(0,m-1):
        new_number = (numbers[i]+numbers[k+i])%m
        numbers.append(new_number)
    numbers = get_normalized_numbers(numbers,m)
    return numbers

def bbs(seed,p,q):
    module = p*q
    numbers = []
    first_number = (seed**2)%module
    actual_number = first_number
    numbers.append(actual_number)
    while True:
        actual_number= (actual_number**2)%module
        if(actual_number == first_number):
            break
        numbers.append(actual_number)
    numbers = get_normalized_numbers(numbers,module)
    return numbers

def get_normalized_numbers(numbers,module):
    normalized_numbers = []
    for num in numbers:
        normalized_numbers.append(num/module)
    return normalized_numbers
