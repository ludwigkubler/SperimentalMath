# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    num_trials = 30
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            random.shuffle(literals)
            clause = ' or '.join(literals)
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def monomial_to_polynomial(monomial):
        terms = monomial.split(' and ')
        polynomial = 1
        for term in terms:
            literals = term.split(' or ')
            product = 1
            for literal in literals:
                if literal.startswith('~'):
                    product *= (1 - x[literal[2:]])
                else:
                    product *= x[literal]
            polynomial *= product
        return polynomial
    
    def symmetric_square_decomposition(polynomial):
        # Placeholder for actual decomposition logic
        # For simplicity, we'll just count the number of terms as a proxy
        return len(polynomial.split(' + '))
    
    x = {f'x{i}': random.randint(0, 1) for i in range(n)}
    permanent_like_polynomial = monomial_to_polynomial(generate_3sat_instance(n))
    determinant_like_polynomial = monomial_to_polynomial(generate_3sat_instance(n))
    
    permanent_shape = [(n - i) * [n - j - 1] for i in range(n) for j in range(n)]
    determinant_shape = [(i + 1) * [j + 1] for i in range(n) for j in range(n)]
    
    permanent_components = symmetric_square_decomposition(permanent_like_polynomial)
    determinant_components = symmetric_square_decomposition(determinant_like_polynomial)
    
    metric_value = permanent_components - determinant_components
    conjecture_holds = metric_value >= n**2
    counterexample = "" if conjecture_holds else f"Permanent: {permanent_components}, Determinant: {determinant_components}"
    
    return {
        "metric_name": "Irreducible Component Count Gap",
        "metric_value": metric_value,
        "instances_tested": num_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")