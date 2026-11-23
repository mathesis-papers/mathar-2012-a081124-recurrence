import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


def binomial_transform(values):
    return [sum(math.comb(index, position) * values[position]
                for position in range(index + 1))
            for index in range(len(values))]


def recurrence_values(initial, endpoint, last_offset):
    values = list(initial)
    for index in range(3, endpoint + 1):
        numerator = (4 * values[index - 1] + (index - 2) * values[index - 2]
                     - (index - last_offset) * values[index - 3])
        assert numerator % 2 == 0, ('divisibility', index, last_offset)
        values.append(numerator // 2)
    return values


def parity_identity(values, parameter, endpoint):
    for index in range(endpoint + 1):
        residual = (2 * values[index + 3] + 2 * values[index + 2]
                    - (index + 3) * values[index + 1]
                    - (index + parameter) * values[index])
        assert residual == 0, ('parity identity', parameter, index)


def multiply(first, second, endpoint):
    return [sum((first[position] * second[degree - position]
                 for position in range(degree + 1)), Fraction(0))
            for degree in range(endpoint + 1)]


def series_checks(first, second, endpoint):
    odd = [Fraction(0)] * (endpoint + 1)
    for degree in range(endpoint):
        forcing = Fraction(1) if degree == 0 else Fraction(0)
        prior = odd[degree - 1] / 2 if degree >= 1 else Fraction(0)
        odd[degree + 1] = (forcing + prior) / (degree + 1)
    underlying = [Fraction(1)] + [odd[degree - 1] / 2
                                for degree in range(1, endpoint + 1)]
    full = [underlying[degree] + odd[degree] for degree in range(endpoint + 1)]
    exponential = [Fraction(1, math.factorial(degree)) for degree in range(endpoint + 1)]
    first_series = multiply(exponential, full, endpoint)
    second_series = multiply(exponential, underlying, endpoint)
    for degree in range(endpoint + 1):
        assert first_series[degree] == Fraction(first[degree], math.factorial(degree))
        assert second_series[degree] == Fraction(second[degree], math.factorial(degree))
        assert second[degree + 1] == first[degree + 1] - first[degree]
        assert first[degree] == sum(second[:degree + 1])


def transform_identities(values, endpoint):
    for index in range(endpoint + 1):
        shifted = [sum(math.comb(index, position) * values[position + shift]
                       for position in range(index + 1)) for shift in range(4)]
        weighted = sum(math.comb(index, position) * position
                       * (values[position + 1] + values[position])
                       for position in range(index + 1))
        assert weighted == index * shifted[1]
        for shift in range(3):
            following = sum(math.comb(index + 1, position) * values[position + shift]
                            for position in range(index + 2))
            assert following == shifted[shift] + shifted[shift + 1]


def main():
    parser = argparse.ArgumentParser(description='Exact finite checks for two factorial binomial transforms.')
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    endpoint = 256
    parity_endpoint = 512
    series_endpoint = 64
    count = parity_endpoint + 4
    full_input = [math.factorial(index // 2) for index in range(count)]
    even_input = [math.factorial(index // 2) if index % 2 == 0 else 0 for index in range(count)]
    first = binomial_transform(full_input[:endpoint + 1])
    second = binomial_transform(even_input[:endpoint + 1])
    assert first == recurrence_values([1, 2, 4], endpoint, 1)
    assert second == recurrence_values([1, 1, 2], endpoint, 2)
    parity_identity(full_input, 1, parity_endpoint)
    parity_identity(even_input, 2, parity_endpoint)
    transform_identities(full_input, series_endpoint)
    transform_identities(even_input, series_endpoint)
    series_checks(first, second, series_endpoint)
    data_path = Path(__file__).with_name('reference-values.json')
    reference = json.loads(data_path.read_text())
    for key, calculated in [('A081124', first), ('A084261', second)]:
        expected = reference[key]['values']
        assert calculated[:len(expected)] == expected, ('OEIS prefix', key)
    result = {
        'status': 'pass',
        'arithmetic': 'Python integers and fractions.Fraction',
        'checks': [
            {'claim': 'A081124 initial values and recurrence-generated terms versus binomial sum',
             'indices': [0, endpoint], 'status': 'pass'},
            {'claim': 'A084261 initial values and recurrence-generated terms versus binomial sum',
             'indices': [0, endpoint], 'status': 'pass'},
            {'claim': 'Both parity identities', 'indices': [0, parity_endpoint], 'status': 'pass'},
            {'claim': 'Pascal and weighted binomial identities for both input sequences',
             'indices': [0, series_endpoint], 'status': 'pass'},
            {'claim': 'Both exponential generating functions, exact coefficients',
             'degrees': [0, series_endpoint], 'status': 'pass'},
            {'claim': 'The mixed relation between the sequences', 'indices': [0, series_endpoint], 'status': 'pass'},
            {'claim': 'OEIS listed sequence prefixes', 'terms': {key: len(value['values'])
                                                             for key, value in reference.items()}, 'status': 'pass'},
        ],
        'sample': {'A081124': first[:12], 'A084261': second[:12]},
        'scope': 'Finite exact-arithmetic checks; all-index proofs are in note.tex.',
        'reference_values_sha256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if arguments.output:
        arguments.output.write_text(serialized)
    print(serialized, end='')


if __name__ == '__main__':
    main()
