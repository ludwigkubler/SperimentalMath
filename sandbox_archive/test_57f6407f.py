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
    
    def generate_linear_equation(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def schur_algebra_rank(f):
        n = len(f)
        A = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(i, n):
                            A[j][i] ^= A[j][i]
        return rank
    
    def construct_circuit(equation, depth):
        if depth == 0:
            return equation
        else:
            left = construct_circuit(equation[:len(equation)//2], depth-1)
            right = construct_circuit(equation[len(equation)//2:], depth-1)
            return [left[i] ^ right[i] for i in range(len(left))]
    
    n = random.randint(5, 40)
    equation = generate_linear_equation(n)
    D = random.randint(1, 10)
    circuit = construct_circuit(equation, D)
    sigma_C = schur_algebra_rank(circuit)
    
    return {
        "metric_name": "sigma_C",
        "metric_value": sigma_C,
        "instances_tested": 1,
        "conjecture_holds": sigma_C >= D**3,
        "counterexample": "" if sigma_C >= D**3 else f"sigma_C={sigma_C} < {D**3}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_sigma_C = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_sigma_C)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_sigma_C} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"sigma_C < D^3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")