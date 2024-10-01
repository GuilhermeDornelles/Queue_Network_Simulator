class Generator:
    def generate_numbers(self, total_number: int, seed: int, multiplier: int, increment: int, module: int, precision: int) -> []:
        current_number = seed
        
        numbers_list = []
        
        for i in range(total_number):
            current_number = self.__randomize(a=multiplier, x=current_number, c=increment, m=module)
            rdn : float = current_number/module
            if (precision != -1):
                rdn = round(rdn,2)
            numbers_list.append(rdn)
        
        return numbers_list
    
    def __randomize(self, a, x, c, m: int) -> int:
        return (a * x + c) % m