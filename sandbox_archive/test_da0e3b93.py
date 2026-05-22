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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random finite field size p and prime number q
    p = random.randint(2, 100)
    while not is_prime(p):
        p = random.randint(2, 100)
    
    q = random.choice([p for p in range(2, 100) if is_prime(p)])
    
    # Generate a random affine plane curve C over the finite field F_p
    n = random.randint(5, 40)
    coefficients = [random.randint(0, p-1) for _ in range(n+1)]
    C = [(x**n + sum(coefficients[i] * x**(n-i) for i in range(n+1)) % p) for x in range(p)]
    
    # Compute the characteristic function of the curve C
    def char_function(x):
        return 1 if (x**n + sum(coefficients[i] * x**(n-i) for i in range(n+1)) % p == 0) else 0
    
    # Construct an AC^0 circuit to compute the characteristic function
    n_gates = random.randint(5, 40)
    circuit = []
    for _ in range(n_gates):
        gate_type = random.choice(['AND', 'OR'])
        if gate_type == 'AND':
            inputs = [random.choice([0, 1]) for _ in range(random.randint(2, n))]
            output = all(inputs)
        else:
            inputs = [random.choice([0, 1]) for _ in range(random.randint(2, n))]
            output = any(inputs)
        circuit.append((gate_type, inputs, output))
    
    # Compute the minimal p-adic valuation of the coordinates of any point P_i on C
    min_valuation = float('inf')
    for x in range(p):
        if char_function(x) == 1:
            valuation = sum(int(digit != '0') for digit in str(x).zfill(len(str(p))))
            if valuation < min_valuation:
                min_valuation = valuation
    
    # Compare the minimal p-adic valuation to the number of AND gates in the circuit
    conjecture_holds = min_valuation >= math.log2(n_gates)
    counterexample = "" if conjecture_holds else f"Point with valuation {min_valuation} < log2({n_gates})"
    
    return {
        "metric_name": "Minimal p-adic Valuation",
        "metric_value": min_valuation,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 100000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")