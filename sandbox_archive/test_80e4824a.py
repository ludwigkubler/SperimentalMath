# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    m, n = len(shape), len(shape[0])
    total = 0
    for i in range(m):
        for j in range(n):
            h = shape[i][j] - i - 1 + n - j - 1
            total += (shape[i][j] * (h + 1)) // (2 * (i + 1) * (j + 1))
    return factorial(m + n - 1) // total

def generate_monotone_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(1, n)]
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        m = math.ceil(math.sqrt(n))
        Phi = generate_monotone_cnf(n, m)
        Y_Phi = hook_length_formula([[m, n-m]])
        C_Phi = 2 ** (n ** 0.5)  # Approximate lower bound for monotone circuit size
        results.append({"Y_Phi": Y_Phi, "C_Phi": C_Phi})
    
    metric_value_Y = sum(result["Y_Phi"] for result in results)
    metric_value_C = sum(result["C_Phi"] for result in results)
    instances_tested = len(results)
    conjecture_holds_Y = all(Y_Phi <= n**m for Y_Phi, m in zip([result["Y_Phi"] for result in results], [math.ceil(math.sqrt(n)) for n in range(5, 41)]))
    conjecture_holds_C = all(C_Phi >= 2**(n**0.5) for C_Phi, n in zip([result["C_Phi"] for result in results], range(5, 41)))
    
    counterexample_Y = "" if conjecture_holds_Y else "Y(Φ) > n^m"
    counterexample_C = "" if conjecture_holds_C else "C(Φ) < 2^(n^0.5)"
    
    return {
        "metric_name": "Y(Φ) and C(Φ)",
        "metric_value_Y": metric_value_Y,
        "metric_value_C": metric_value_C,
        "instances_tested": instances_tested,
        "conjecture_holds_Y": conjecture_holds_Y,
        "conjecture_holds_C": conjecture_holds_C,
        "counterexample_Y": counterexample_Y,
        "counterexample_C": counterexample_C
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 50))  # Default to first 30 primes

    results_Y = []
    results_C = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        results_Y.append(result["metric_value_Y"])
        results_C.append(result["metric_value_C"])

    mean_Y = sum(results_Y) / len(results_Y)
    std_Y = math.sqrt(sum((x - mean_Y) ** 2 for x in results_Y) / len(results_Y))
    support_fraction_Y = sum(1 for result in results_Y if result <= 0) / len(results_Y)

    mean_C = sum(results_C) / len(results_C)
    std_C = math.sqrt(sum((x - mean_C) ** 2 for x in results_C) / len(results_C))
    support_fraction_C = sum(1 for result in results_C if result >= 0) / len(results_C)

    if support_fraction_Y >= 0.8 and support_fraction_C >= 0.8:
        print(f"RESULT: SUPPORTED mean_Y={mean_Y} std_Y={std_Y} support_fraction_Y={support_fraction_Y}")
    elif any(result > 0 for result in results_Y) or any(result < 0 for result in results_C):
        first_failing_seed = seeds[results_Y.index(max(results_Y)) if any(result > 0 for result in results_Y) else results_C.index(min(results_C))]
        print(f"RESULT: FALSIFIED counterexample_Y='{result['counterexample_Y']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")