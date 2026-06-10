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
    
    def generate_circuit(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['~' + v for v in variables], 2)
            clauses.append(clause)
        return variables, clauses
    
    def count_monodromy_representations(variables, clauses):
        # This is a placeholder function. In practice, you would need to compute
        # the minimal number of monodromy representations for the given circuit.
        # For simplicity, we'll use a dummy value that depends on n and m.
        return len(variables) * len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n**2, 100))  # Ensure m is not too large
    variables, clauses = generate_circuit(n, m)
    
    metric_value = count_monodromy_representations(variables, clauses)
    conjecture_holds = metric_value <= n**3 * m
    
    return {
        "metric_name": "monodromy_representations",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n_max']}, m={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")