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

class bbs_generator(congruencial_generator):
    def __init__(self, seed, p, q):
        super().__init__(seed, p*q, 1)
        self.numbers = []
        self.normalized_numbers = []

    #x^2 % m
    def calculate_next_number(self, actual_number):
        return (actual_number**2)%self.module

class additive_generator(congruencial_generator):
    def __init__(self, parameters, k,module):
        super().__init__(parameters[0], module, 1)
        self.parameters = parameters
        self.k = k

    def generate_numbers(self):
        self.numbers = self.parameters
        for i in range(0,self.module-1):
            next_number = (self.numbers[i]+self.numbers[self.k+i])%self.module
            self.numbers.append(next_number)
        return self.numbers
