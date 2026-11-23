import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def even_transform(index, parameter):
    return sum(math.comb(index, 2 * position) * math.factorial(position)
               * parameter ** (index - 2 * position)
               for position in range(index // 2 + 1))


def full_transform(index, parameter):
    return sum(math.comb(index, position) * math.factorial(position // 2)
               * parameter ** (index - position)
               for position in range(index + 1))


def rising_factorial(start, length):
    return math.prod(range(start, start + length))


def determinant(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            result = -result
        value = matrix[column][column]
        result *= value
        for row in range(column + 1, len(matrix)):
            multiplier = matrix[row][column] / value
            for following in range(column + 1, len(matrix)):
                matrix[row][following] -= multiplier * matrix[column][following]
    return result


def continued_fraction(parameter, endpoint):
    tail = [Fraction(1)] + [Fraction(0)] * endpoint
    for height in range(endpoint // 2, -1, -1):
        weight = (height + 2) // 2
        current = [Fraction(1)] + [Fraction(0)] * endpoint
        for degree in range(1, endpoint + 1):
            current[degree] = parameter * current[degree - 1]
            if degree >= 2:
                current[degree] += weight * sum(tail[position] * current[degree - 2 - position]
                                                for position in range(degree - 1))
        tail = current
    return tail


def main():
    parser = argparse.ArgumentParser(description='Exact checks for weighted factorial transforms and linked formulas.')
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    endpoint = 64
    shorter_endpoint = 128
    array_endpoint = 48
    parameters = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2)]
    for parameter in parameters:
        even = [even_transform(index, parameter) for index in range(endpoint + 1)]
        full = [full_transform(index, parameter) for index in range(endpoint + 1)]
        assert even[:3] == [1, parameter, parameter ** 2 + 1]
        for index in range(3, endpoint + 1):
            assert (2 * even[index] - 4 * parameter * even[index - 1]
                    + (2 * parameter ** 2 - index) * even[index - 2]
                    + (index - 2) * parameter * even[index - 3]) == 0
        for index in range(endpoint + 1):
            assert full[index] == even[index] + sum(parameter ** (index - 1 - position) * even[position]
                                                   for position in range(index))
            coefficients = [math.comb(index, position) * math.factorial((index - position) // 2)
                            if (index - position) % 2 == 0 else 0
                            for position in range(index + 1)]
            assert sum(coefficients[position] * parameter ** position
                       for position in range(index + 1)) == even[index]
        assert continued_fraction(parameter, endpoint) == even
        for index in range(13):
            matrix = [[even[row + column] for column in range(index + 1)]
                      for row in range(index + 1)]
            product = math.prod(((position + 2) // 2) ** (index - position)
                                for position in range(index + 1))
            assert determinant(matrix) == product
    full_at_one = [full_transform(index, Fraction(1)) for index in range(shorter_endpoint + 1)]
    even_at_one = [even_transform(index, Fraction(1)) for index in range(shorter_endpoint + 1)]
    for index in range(2, shorter_endpoint + 1):
        assert 2 * (even_at_one[index] - 1) == index * full_at_one[index - 2]
        assert 2 * (full_at_one[index] - 1 - full_at_one[index - 1]) == index * full_at_one[index - 2]
    array = [[sum(math.comb(first, position) * math.comb(second, position) * math.factorial(position)
                  for position in range(min(first, second) + 1))
              for second in range(array_endpoint + 1)] for first in range(array_endpoint + 1)]
    for first in range(array_endpoint + 1):
        for second in range(array_endpoint + 1):
            assert array[first][second] == array[second][first]
            if first:
                expected = array[first - 1][second]
                if second:
                    expected += second * array[first - 1][second - 1]
                assert array[first][second] == expected
            else:
                assert array[first][second] == 1
    for index in range(array_endpoint + 1):
        assert sum(array[first][index - first] for first in range(index + 1)) == full_at_one[index]
    for index in range(513):
        product = math.prod(range(1, index // 2 + 1))
        assert product == math.factorial(index // 2)
        companion = math.factorial(index) // math.factorial(index // 2)
        corrected_product = math.prod(range(index // 2 + 1, index + 1))
        assert corrected_product == companion
        assert rising_factorial(index // 2 + 1, (index + 1) // 2) == companion
        swinging = math.factorial(index) // math.factorial(index // 2) ** 2
        assert companion == math.factorial(index // 2) * swinging
        assert companion ** 2 == math.factorial(index) * swinging
        coefficient = Fraction(1, math.factorial(index // 2))
        assert Fraction(companion, math.factorial(index)) == coefficient
        if index >= 3:
            prior = [math.factorial(index - offset) // math.factorial((index - offset) // 2)
                     for offset in range(4)]
            assert prior[0] + 2 * prior[1] - 2 * index * prior[2] + 4 * (2 - index) * prior[3] == 0
    assert math.prod(range((2 + 1) // 2, 2)) == 1
    assert rising_factorial((2 + 1) // 2, 2 // 2) == 1
    assert math.factorial(2) // math.factorial(2 // 2) == 2
    result = {
        'status': 'pass',
        'arithmetic': 'Python integers and fractions.Fraction',
        'parameters': [str(parameter) for parameter in parameters],
        'checks': [
            {'claim': 'Weighted recurrence and initial values', 'indices': [0, endpoint], 'status': 'pass'},
            {'claim': 'Weighted partial-sum identity', 'indices': [0, endpoint], 'status': 'pass'},
            {'claim': 'A161556 row polynomials', 'rows': [0, endpoint], 'status': 'pass'},
            {'claim': 'Formal Jacobi continued-fraction coefficients', 'degrees': [0, endpoint], 'status': 'pass'},
            {'claim': 'Hankel determinant product', 'determinant_indices': [0, 12], 'status': 'pass'},
            {'claim': 'Both shorter inhomogeneous recurrences', 'indices': [2, shorter_endpoint], 'status': 'pass'},
            {'claim': 'Somos array formula, symmetry, boundary and recurrence',
             'coordinate_ranges': [[0, array_endpoint], [0, array_endpoint]], 'status': 'pass'},
            {'claim': 'Somos array antidiagonal sums equal A081124', 'indices': [0, array_endpoint], 'status': 'pass'},
            {'claim': 'Two-part partition product and factorial-ratio EGF coefficients', 'indices': [0, 512], 'status': 'pass'},
            {'claim': 'A081125 factorial-ratio recurrence', 'indices': [3, 512], 'status': 'pass'},
            {'claim': 'Corrected interval product, rising factorial and swinging-factorial forms', 'indices': [0, 512], 'status': 'pass'},
            {'claim': 'A081125 recorded interval product and SageMath formula fail at n=2; corrected product is 2',
             'index': 2, 'recorded_product': 1, 'factorial_quotient': 2, 'status': 'pass'},
        ],
        'scope': 'Finite exact-arithmetic checks; the all-index identities have written proofs in note.tex.',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(serialized)
    print(serialized, end='')


if __name__ == '__main__':
    main()
