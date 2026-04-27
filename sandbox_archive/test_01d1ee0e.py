# auto-injected by SEC sandbox
import itertools
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def hamming_weight(x):
    return bin(x).count('1')

def truth_table(f, n):
    return [f(tuple(bin(i)[2:].zfill(n))) for i in range(2**n)]

def A_w(f, w):
    return sum(f(x) * (-1)**hamming_weight(x) for x in range(2**len(f)) if hamming_weight(x) == w) / binomial(len(f), w)

def sigma(f):
    n = len(f)
    return sum(A_w(f, w) * math.log2(binomial(n, w)) for w in range(n + 1))

def Var(f):
    n = len(f)
    mean = sum(x * f(x) for x in range(2**n)) / 2**n
    return sum((x - mean)**2 * f(x) for x in range(2**n)) / 2**n

def S_2(f, max_size=8):
    n = len(f)
    if n <= 3:
        # Brute-force search for depth-3 ACC^0[2] circuits
        def is_acc02(circuit):
            stack = []
            for gate in circuit:
                if gate == 'MOD2':
                    if not stack or stack[-1] != 'AND':
                        return False
                    stack.pop()
                elif gate == 'AND':
                    stack.append(gate)
                else:
                    return False
            return len(stack) == 0
        min_size = float('inf')
        for size in range(1, max_size + 1):
            for circuit in itertools.product(['MOD2', 'AND'], repeat=size):
                if is_acc02(circuit):
                    min_size = min(min_size, size)
        return min_size
    else:
        # Layered SAT-free brute-force enumerator
        def evaluate_circuit(circuit, x):
            stack = []
            for gate in reversed(circuit):
                if gate == 'MOD2':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append((a + b) % 2)
                elif gate == 'AND':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a & b)
            return stack[0]
        min_size = float('inf')
        for size in range(1, max_size + 1):
            for circuit in itertools.product(['MOD2', 'AND'], repeat=size):
                if evaluate_circuit(circuit, tuple(random.randint(0, 1) for _ in range(n))) == f(tuple(random.randint(0, 1) for _ in range(n))):
                    min_size = min(min_size, size)
        return min_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5] + list(range(6, 13))
    instances_tested = 0
    support_fraction = 0.0
    max_violation_ratio = 0.0
    counterexample = ""

    for n in n_values:
        if n <= 5:
            functions = [lambda x: random.choice([0, 1]) for _ in range(2**n)]
        else:
            functions = [truth_table(lambda x: random.choice([0, 1]), n) for _ in range(2000)]

        for f in functions:
            instances_tested += 1
            A_w_values = [A_w(f, w) for w in range(n + 1)]
            sigma_f = sigma(f)
            Var_value = Var(f)
            S_2_value = S_2(f)

            if sigma_f == 0 or S_2_value == 0:
                continue

            r_f = Var_value / ((n + 1) * abs(sigma_f) * math.log2(1 + S_2_value))
            support_fraction += r_f <= 1.0
            max_violation_ratio = max(max_violation_ratio, r_f)

            if r_f > 1.0:
                counterexample = f"n={n}, Var/((n+1)|σ(f)|·log2(1+S_2))={r_f}"

    conjecture_holds = support_fraction >= 0.99 and max_violation_ratio <= 1.0
    return {
        "metric_name": "max_violation_ratio",
        "metric_value": max_violation_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max_violation_ratio > 1.0:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")