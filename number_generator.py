#a*x % m
class congruencial_generator:
    def __init__(self,seed, module, multiplicative):
        self.seed = seed
        self.module = module
        self.multiplicative = multiplicative
        self.numbers = []
        self.normalized_numbers = []

    def get_normalized_numbers(self):
        if not self.numbers:
            self.generate_numbers()
        if not self.normalized_numbers:
            self.normalized_numbers = [num / self.module for num in self.numbers]
        return self.normalized_numbers

    def calculate_next_number(self, actual_number):
        return (self.multiplicative*actual_number)%self.module

    def generate_numbers(self):
        first_number = self.calculate_next_number(self.seed)
        actual_number = first_number
        self.numbers.append(actual_number)
        while True:
            actual_number = self.calculate_next_number(actual_number)
            if(actual_number == first_number):
                break
            self.numbers.append(actual_number)
        return self.numbers

#a*x+c % m
class congruencial_mixto_generator(congruencial_generator):
    def __init__(self, seed, module, multiplicative, additive):
        super().__init__(seed, module, multiplicative)
        self.additive = additive

    def calculate_next_number(self, actual_number):
        return ((self.multiplicative*actual_number)+self.additive)%self.module

#a*x^2+b*x+c % m
class congruencial_cuadratico_generator(congruencial_generator):
    def __init__(self, seed, module, a,b,c):
        super().__init__(seed, module, a)
        self.b = b
        self.c = c

    def calculate_next_number(self, actual_number):
        return (self.a*(self.seed**2)+self.b*self.seed+self.c)%self.module

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
