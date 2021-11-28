import copy


class Node:
    def __init__(self, coef, exp):
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

    def negative(self):
        for i in range(self.start, self.finish + 1):
            Polynomial.elements[i].coef *= -1

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

        return result

    def minus(self, other):
        self.negative()
        return self.plus(other)

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

    @staticmethod
    def plus_minus_handler(b1, b2, operator):
        if operator == '-':
            b2.sign = not b2.sign
        if b1.sign and b2.sign:
            result = b1.plus(b2)
            result.sign = True
            return result
        if not b1.sign and not b2.sign:
            result = b1.plus(b2)
            result.sign = False
            return result
        compare_result = b1.compare(b2)
        if compare_result == 1:
            result = b1.minus(b2)
            result.sign = b1.sign
            return result
        if compare_result == -1:
            result = b2.minus(b1)
            result.sign = b2.sign
            return result
        return BigNumber('0')

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

    def increase(self):
        return self.plus(BigNumber('1'))

    def decrease(self):
        return self.minus(BigNumber('1'))

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


if __name__ == "__main__":
    p1 = Polynomial()
    p1.add(2, 1)
    p1.add(1, 0)
    p2 = Polynomial()
    p2.add(3, 1)
    p2.add(1, 0)
    p3 = p1.times(p2)
    p3.print_polynomial()
