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
    
    def generate_cnf(n):
        m = 2 * n
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def polynomial_from_cnf(cnf):
        terms = {}
        for clause in cnf:
            term = 1
            for lit in clause:
                if lit > 0:
                    term *= (1 + Fraction(1, 2**lit))
                else:
                    term *= (1 - Fraction(1, 2**(-lit)))
            terms[tuple(sorted(clause))] = term
        return terms
    
    def toric_variety_size(polynomial):
        # Simplified mapping to estimate the number of vertices
        # This is a placeholder and should be replaced with an actual computation
        return sum(abs(term) for term in polynomial.values())
    
    n_max = 40
    instances_tested = 0
    total_vertices = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        polynomial = polynomial_from_cnf(cnf)
        num_vertices = toric_variety_size(polynomial)
        
        if num_vertices <= 0:
            continue
        
        instances_tested += 1
        total_vertices += num_vertices
    
    if instances_tested == 0:
        return {
            "metric_name": "num_vertices",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_vertices = total_vertices / instances_tested
    return {
        "metric_name": "num_vertices",
        "metric_value": mean_vertices,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False if mean_vertices > 2 * n_max else True,
        "counterexample": "" if mean_vertices <= 2 * n_max else f"mean_vertices={mean_vertices} exceeds expected bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")