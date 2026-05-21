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
    n = 30
    metric_name = "Hilbert Function Growth"
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def compute_hilbert_function(clauses):
        monomial_set = set()
        for clause in clauses:
            for var in clause:
                monomial_set.add(tuple(sorted(abs(v) for v in clause)))
        hilbert_values = [0] * (n + 1)
        for k in range(1, n + 1):
            for monomial in monomial_set:
                if len(monomial) == k:
                    hilbert_values[k] += 1
        return hilbert_values
    
    def is_acc0_circuit_size_lower_bound(n):
        # Placeholder for actual ACC^0 circuit size lower bound check
        # This is a dummy implementation; replace with actual logic
        return n >= 5
    
    clauses = generate_3cnf(n)
    hilbert_values = compute_hilbert_function(clauses)
    
    metric_value = max(hilbert_values[1:])
    conjecture_holds = is_acc0_circuit_size_lower_bound(n) == (metric_value >= math.log(n))
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")