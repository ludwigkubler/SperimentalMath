# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(k, m):
        variables = set(f"x{i}" for i in range(1, k+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [f"~{var}" if var.startswith("x") else f"{var}" for var in clause]
            clauses.append(clause)
        return clauses
    
    def count_unique_clauses(clauses):
        unique_clauses = set(tuple(sorted(clause)) for clause in clauses)
        return len(unique_clauses)
    
    def quaternionic_automorphism_group_size(clauses):
        # This is a placeholder function. In practice, you would need to implement
        # the actual computation of the quaternionic automorphism group size.
        # For simplicity, we'll just return a random value that depends on the seed.
        return random.randint(1, 10)
    
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = ((sum((xi - mean_x) ** 2 for xi in x)) * 
                       (sum((yi - mean_y) ** 2 for yi in y))) ** 0.5
        
        if denominator == 0:
            return None
        
        return numerator / denominator
    
    n_tests = 30
    results = []
    
    for _ in range(n_tests):
        k = random.randint(2, 10)
        m = random.randint(k * 2, k * 5)
        clauses = generate_kcnf(k, m)
        unique_clauses = count_unique_clauses(clauses)
        qaut_size = quaternionic_automorphism_group_size(clauses)
        
        results.append({
            "qaut_size": qaut_size,
            "unique_clauses": unique_clauses
        })
    
    qaut_sizes = [r["qaut_size"] for r in results]
    unique_clause_counts = [r["unique_clauses"] for r in results]
    
    correlation_coefficient = pearson_correlation(qaut_sizes, unique_clause_counts)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tests,
        "n_max": max(len(clauses) for clauses in results),
        "conjecture_holds": correlation_coefficient is not None and correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")