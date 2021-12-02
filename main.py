import copy


class BigNumber:

    def __init__(self, number_str):
        self.sign = True
        if number_str[0] == '-':
            self.sign = False
            number_str = number_str[1:]
        self.num_array = list(map(int, reversed(number_str)))

    def clone(self):
        return copy.deepcopy(self)

    def remove_extra_zeros(self):
        self.num_array = list(map(int, reversed(str(self))))

    def __str__(self):
        number_str = ''.join(map(str, self.num_array))[::-1]
        if all(ch == '0' for ch in number_str):
            return '0'
        return number_str.lstrip('0')

    @classmethod
    def zero(cls, n):
        zero = cls('0')
        for _ in range(n - 1):
            zero.num_array.append(0)
        return zero

    def __getitem__(self, key):
        return self.num_array[key]

    def __setitem__(self, key, value):
        self.num_array[key] = value

    def to_int(self):
        number_str = str(self)
        if number_str == '0':
            return 0
        number = int(number_str.lstrip('0'))
        return number if self.sign else number * -1

    def append_zero(self, n):
        for _ in range(n):
            self.num_array.append(0)

    def shift_right(self, n=1):
        clone = self.clone()
        for _ in range(n):
            clone.num_array.pop(0)
        return clone

    def shift_left(self, n=1):
        clone = self.clone()
        for _ in range(n):
            clone.num_array.insert(0, 0)
        return clone

    def compare(self, other):
        s1 = str(self)
        s2 = str(other)
        if len(s1) > len(s2):
            return 1
        elif len(s2) > len(s1):
            return -1
        for n1, n2 in zip(s1, s2):
            if n1 > n2:
                return 1
            elif n2 > n1:
                return -1
        return 0

    def plus(self, other):
        n1, n2 = len(self.num_array), len(other.num_array)
        result_length = max(n1, n2) + 1
        result = BigNumber.zero(result_length)
        self.append_zero(result_length - n1)
        other.append_zero(result_length - n2)
        carry = 0
        for i in range(result_length):
            sum_result = self[i] + other[i] + carry
            result[i] = sum_result % 10
            carry = sum_result // 10

        return result

    def __add__(self, other):
        return self.plus(other)

    def minus(self, other):
        n1, n2 = len(self.num_array), len(other.num_array)
        result_length = max(n1, n2)
        result = BigNumber.zero(result_length)
        self.append_zero(result_length - n1)
        other.append_zero(result_length - n2)
        for i in range(result_length):
            if self[i] < other[i]:
                self[i + 1] -= 1
                self[i] += 10

            result[i] = self[i] - other[i]
        return result

    def __sub__(self, other):
        comparison = self.compare(other)
        if comparison == 1:
            return self.minus(other)
        elif comparison == -1:
            return -other.unsigned_minus(self)
        return BigNumber('0')

    def increase(self):
        return self.plus(BigNumber('1'))

    def decrease(self):
        return self.minus(BigNumber('1'))

    def __mul__(self, other):
        return self.times(other)

    def times(self, other):
        n1, n2 = len(self.num_array), len(other.num_array)
        result = BigNumber.zero(1)
        self.append_zero(1)
        for i in range(n2):
            big_temp = BigNumber.zero(n1 + 1)
            carry = 0
            for j in range(n1 + 1):
                temp_result = other[i] * self[j] + carry
                big_temp[j] = temp_result % 10
                carry = temp_result // 10
            big_temp = big_temp.shift_left(i)
            result = result.plus(big_temp)
        result.sign = not (self.sign ^ other.sign)
        return result

    def __pow__(self, power, modulo=None):
        return self.to_the_power_of(power)

    def __lt__(self, other):
        return self.compare(other) == -1

    def __gt__(self, other):
        return self.compare(other) == 1

    def __neg__(self):
        result = self.clone()
        result.sign = not result.sign
        return result

    def to_the_power_of(self, other):
        other_number = other.to_int()
        if other_number == 0:
            return BigNumber('1')
        elif other_number == 1:
            return self
        result = self.times(self)
        for _ in range(other_number - 2):
            self.remove_extra_zeros()
            result.remove_extra_zeros()
            result = result.times(self)
        return result


class Node:
    def __init__(self, coef: BigNumber, exp: BigNumber):
        self.coef = coef
        self.exp = exp

    def __repr__(self):
        return f"({self.coef} , {self.exp})"


class Polynomial:
    available = 0
    elements = list()

    def __init__(self):
        self.start = None
        self.finish = None

    def print_polynomial(self):
        for i in range(self.start, self.finish + 1):
            print(Polynomial.elements[i], end=" ")
        print()

    def get_value(self, x):
        result = 0
        x_big_number = BigNumber(str(x))
        for i in range(self.start, self.finish + 1):
            result += (x_big_number ** Polynomial.elements[i].exp * Polynomial.elements[i].coef).to_int()

        return result

    def add(self, coef, exp):
        node = Node(coef, exp)
        if self.start is None:
            self.start = self.finish = Polynomial.available
            self.elements.append(node)
        else:
            for i in range(self.finish, self.start - 1, -1):
                if Polynomial.elements[i].exp == exp:
                    Polynomial.elements[i].coef += coef
                    break
                elif Polynomial.elements[i].exp > exp:
                    Polynomial.elements.insert(i + 1, node)
                    self.finish += 1
                    break
        Polynomial.available += 1

    def remove(self, coef, exp):
        node = Node(coef, exp)
        for i in range(self.start, self.finish + 1):
            if node == Polynomial.elements[i]:
                Polynomial.elements.pop(i)
                break

    def plus(self, other):
        result = Polynomial()
        i = self.start
        j = other.start
        while i <= self.finish and j <= other.finish:
            if Polynomial.elements[i].exp < Polynomial.elements[j].exp:
                result.add(other.elements[j].coef, other.elements[j].exp)
                j += 1
            elif Polynomial.elements[i].exp > Polynomial.elements[j].exp:
                result.add(Polynomial.elements[i].coef, Polynomial.elements[i].exp)
                i += 1
            else:
                result.add(Polynomial.elements[i].coef + other.elements[j].coef, Polynomial.elements[i].exp)
                i += 1
                j += 1
        while i <= self.finish:
            result.add(Polynomial.elements[i].coef, Polynomial.elements[i].exp)
            i += 1
        while j <= other.finish:
            result.add(other.elements[j].coef, other.elements[j].exp)
            j += 1

        return result

    def minus(self, other):
        result = Polynomial()
        i = self.start
        j = other.start
        while i <= self.finish and j <= other.finish:
            if Polynomial.elements[i].exp < Polynomial.elements[j].exp:
                result.add(-other.elements[j].coef, other.elements[j].exp)
                j += 1
            elif Polynomial.elements[i].exp > Polynomial.elements[j].exp:
                result.add(Polynomial.elements[i].coef, Polynomial.elements[i].exp)
                i += 1
            else:
                result.add(Polynomial.elements[i].coef - other.elements[j].coef, Polynomial.elements[i].exp)
                i += 1
                j += 1
        while i <= self.finish:
            result.add(Polynomial.elements[i].coef, Polynomial.elements[i].exp)
            i += 1
        while j <= other.finish:
            result.add(-other.elements[j].coef, other.elements[j].exp)
            j += 1
        return result

    def times(self, other):
        result = Polynomial()
        for i in range(self.start, self.finish + 1):
            for j in range(other.start, other.finish + 1):
                result.add(Polynomial.elements[i].coef * Polynomial.elements[j].coef,
                           Polynomial.elements[i].exp + Polynomial.elements[j].exp)
        return result

    def is_zero(self):
        if self.start is None:
            return True
        for i in range(self.start, self.finish + 1):
            if not Polynomial.elements[i] == 0:
                return False
        return True

    def get_coef(self, exp):
        for i in range(self.start, self.finish + 1):
            if Polynomial.elements[i].exp == exp:
                return Polynomial.elements[i].coef
        return None

    def get_maximum_exp(self):
        if self.start is None:
            return None
        return Polynomial.elements[self.start].exp


class Ghati:
    results = list()
    polynomial_inputs = list()
    big_number_inputs = list()
    unknown_value = None
    target = None
    index = None

    @classmethod
    def init(cls):
        for _ in range(int(input())):
            cls.polynomial_inputs.append(input())
        for _ in range(int(input())):
            cls.big_number_inputs.append(input())
        cls.unknown_value = int(input())
        cls.target = int(input())

    @classmethod
    def calculate_big_number_operations(cls):
        for string in cls.big_number_inputs:
            data = string.split(" ")
            big_number = BigNumber(data[0])
            if data[1] == '++':
                cls.results.append(big_number.increase().to_int())
            elif data[1] == '--':
                cls.results.append(big_number.decrease().to_int())
            elif data[1] == 'R':
                cls.results.append(big_number.shift_right().to_int())
            else:
                cls.results.append(big_number.shift_left().to_int())

    @classmethod
    def calculate_polynomial_operations(cls):
        for string in cls.polynomial_inputs:
            data = string.split("(")
            p1 = Polynomial()
            p1_data, operator = data[1].split(')')
            p1_data = p1_data.split('+')
            for node_string in p1_data:
                p1.add(*cls.parse_node(node_string.strip()))
            p2 = Polynomial()
            p2_data = data[2].split(')')[0].split('+')
            for node_string in p2_data:
                p2.add(*cls.parse_node(node_string.strip()))
            operator = operator.strip()
            if operator == '+':
                cls.results.append(p1.plus(p2).get_value(cls.unknown_value))
            elif operator == '-':
                cls.results.append(p1.minus(p2).get_value(cls.unknown_value))
            else:
                cls.results.append(p1.times(p2).get_value(cls.unknown_value))

    @staticmethod
    def parse_node(node_string):
        coef, exp = node_string.split('x^')
        return BigNumber(coef), BigNumber(exp)

    @classmethod
    def sort_results(cls):
        cls.results.sort()

    @classmethod
    def find_target(cls):
        return cls.binary_search(cls.results, 0, len(cls.results) - 1, cls.target)

    @staticmethod
    def binary_search(arr, low, high, x):
        if low <= high:
            mid = (high + low) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] > x:
                return Ghati.binary_search(arr, low, mid - 1, x)
            return Ghati.binary_search(arr, mid + 1, high, x)
        return -1


if __name__ == "__main__":
    Ghati.init()
    Ghati.calculate_polynomial_operations()
    Ghati.calculate_big_number_operations()
    Ghati.sort_results()
    print(Ghati.find_target())
