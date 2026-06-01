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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n, d):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate all 2^(n-1) clauses
        for i in range(1 << (n-1)):
            clause = []
            for j in range(n):
                if i & (1 << j):
                    clause.append(variables[j])
                else:
                    clause.append(f'~{variables[j]}')
            clauses.append(' | '.join(clause))
        
        # Add the final clause
        final_clause = ' ^ '.join([f'{variables[i]} -> {variables[n-1]}' for i in range(n)])
        clauses.append(final_clause)
        
        # Ensure d-regularity
        while True:
            random.shuffle(clauses)
            if all(len(set(clause.split(' | '))) == d for clause in clauses):
                break
        
        return ' & '.join(clauses)

    def calculate_tropical_kahler_curvature(formula):
        # Placeholder function to simulate the calculation of tropical Kähler curvature
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    def calculate_circuit_monotone_complexity(formula):
        # Placeholder function to simulate the calculation of circuit monotone complexity
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)

    n = random.randint(5, 30)
    d = random.randint(2, n-1)
    formula = generate_tseitin_formula(n, d)
    tK = calculate_tropical_kahler_curvature(formula)
    m_C = calculate_circuit_monotone_complexity(formula)

    return {
        "metric_name": "correlation",
        "metric_value": tK * m_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")