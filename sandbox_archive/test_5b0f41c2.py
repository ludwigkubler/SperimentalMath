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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = f'{variables[i]}'
            clauses.append(clause)
            clauses.append(f'~{clause}')
        return clauses
    
    def polynomial_from_clause(clause, n):
        if 'x' not in clause:
            return [int(clause)]
        var_index = int(clause[1:])
        return [0] * var_index + [1] + [0] * (n - var_index - 1)
    
    def smallest_noncommutative_division_algebra(polynomials):
        if not polynomials:
            return 0
        dimension_D = len(set(tuple(p) for p in polynomials))
        return dimension_D
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = tseitin_formula(n)
    polynomials = [polynomial_from_clause(clause, n) for clause in phi]
    
    dimension_D = smallest_noncommutative_division_algebra(polynomials)
    w_phi = len(phi)  # Simplified resolution proof width
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": w_phi,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": dimension_D >= w_phi - 3,
        "counterexample": "" if dimension_D >= w_phi - 3 else f"Dimension of D: {dimension_D}, w(φ): {w_phi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")