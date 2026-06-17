"""Simple calculator tool: safely evaluate arithmetic expressions."""
import ast
import operator as op
from datetime import datetime


_operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}


def _eval(node):
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.UnaryOp):
        return _operators[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp):
        return _operators[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")


def calculate(expression: str):
    """Safely calculate a simple arithmetic expression and return result.

    Raises ValueError on invalid expressions.
    Also logs the call with a timestamp when run as a tool.
    """
    ts = datetime.utcnow().isoformat() + "Z"
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
        return {"input": expression, "result": result, "time": ts}
    except Exception as e:
        return {"input": expression, "error": str(e), "time": ts}


if __name__ == "__main__":
    print(calculate("2+3*4"))
def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):   
    return a * b

def division(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def exponentiation(a, b):
    return a ** b

def modulus(a, b):
    if b == 0:
        raise ValueError("Cannot perform modulus by zero")
    return a % b

def floor_division(a, b):
    if b == 0:
        raise ValueError("Cannot perform floor division by zero")
    return a // b

def square_root(a):
    if a < 0:
        raise ValueError("Cannot compute square root of a negative number")
    return a ** 0.5

def square(a):
    return a ** 2

def logarithm(a, base=10):
    import math
    if a <= 0:
        raise ValueError("Cannot compute logarithm of non-positive numbers")
    return math.log(a, base)

def floor(a):
    import math
    return math.floor(a)

def ceil(a):
    import math
    return math.ceil(a)

def absolute(a):
    return abs(a)

def factorial(n):
    if n < 0:
        raise ValueError("Cannot compute factorial of a negative number")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def gcd(a, b):
    import math
    return math.gcd(a, b)

def lcm(a, b):
    import math
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def percentage(part, whole):
    if whole == 0:
        raise ValueError("Cannot calculate percentage with a whole of zero")
    return (part / whole) * 100

def mean(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot compute mean of an empty list")
    return sum(numbers) / len(numbers)

def median(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot compute median of an empty list")
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]
    
def mode(numbers):
    from collections import Counter
    if len(numbers) == 0:
        raise ValueError("Cannot compute mode of an empty list")
    count = Counter(numbers)
    mode_data = count.most_common()
    max_count = mode_data[0][1]
    modes = [num for num, freq in mode_data if freq == max_count]
    return modes

def variance(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot compute variance of an empty list")
    mean_value = mean(numbers)
    return sum((x - mean_value) ** 2 for x in numbers) / len(numbers)

def standard_deviation(numbers):
    import math
    return math.sqrt(variance(numbers))

def z_score(value, mean_value, std_dev):
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero for z-score calculation")
    return (value - mean_value) / std_dev

def percentile(numbers, percent):
    if len(numbers) == 0:
        raise ValueError("Cannot compute percentile of an empty list")
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    sorted_numbers = sorted(numbers)
    k = (len(sorted_numbers) - 1) * (percent / 100)
    f = int(k)
    c = k - f
    if f + 1 < len(sorted_numbers):
        return sorted_numbers[f] + c * (sorted_numbers[f + 1] - sorted_numbers[f])
    else:
        return sorted_numbers[f]
    
def permutation(n, r):
    if n < 0 or r < 0:
        raise ValueError("n and r must be non-negative")
    if r > n:
        return 0
    result = 1
    for i in range(n, n - r, -1):
        result *= i
    return result

def combination(n, r):
    if n < 0 or r < 0:
        raise ValueError("n and r must be non-negative")
    if r > n:
        return 0
    return permutation(n, r) // factorial(r)

def logarithm_base_e(a):
    import math
    if a <= 0:
        raise ValueError("Cannot compute logarithm of non-positive numbers")
    return math.log(a)

def logarithm_base_2(a):
    import math
    if a <= 0:
        raise ValueError("Cannot compute logarithm of non-positive numbers")
    return math.log2(a)

def rms(values):
    import math
    if len(values) == 0:
        raise ValueError("Cannot compute RMS of an empty list")
    return math.sqrt(sum(x ** 2 for x in values) / len(values))

def geometric_mean(numbers):
    import math
    if len(numbers) == 0:
        raise ValueError("Cannot compute geometric mean of an empty list")
    product = 1
    for num in numbers:
        product *= num
    return product ** (1 / len(numbers))

def harmonic_mean(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot compute harmonic mean of an empty list")
    reciprocal_sum = sum(1 / num for num in numbers)
    return len(numbers) / reciprocal_sum

def weighted_mean(values, weights):
    if len(values) != len(weights):
        raise ValueError("Values and weights must be of the same length")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    return sum(value * weight for value, weight in zip(values, weights)) / total_weight
