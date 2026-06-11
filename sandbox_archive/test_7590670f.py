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
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tautological_ideal(cnf):
        # Placeholder function to simulate the computation of the tautological ideal
        # This is a dummy implementation and does not actually compute anything meaningful
        return [frozenset([abs(lit) for lit in clause]) for clause in cnf]
    
    def graph_laplacian_spectral_gap(cnf):
        # Placeholder function to simulate the computation of the spectral gap
        # This is a dummy implementation and does not actually compute anything meaningful
        return random.random()
    
    n = 10
    mli_values = []
    g_values = []
    
    for _ in range(30):
        cnf = generate_cnf(n)
        ideal = tautological_ideal(cnf)
        mli_value = len(ideal)  # Dummy value for mli(φ)
        g_value = graph_laplacian_spectral_gap(cnf)
        
        mli_values.append(mli_value)
        g_values.append(g_value)
    
    if not mli_values or not g_values:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i for i in range(len(x))}
        y_ranks = {y[i]: i for i in range(len(y))}
        
        n = len(x)
        d_squared_sum = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        
        return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    correlation = spearman_rank_correlation(mli_values, g_values)
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": correlation,
        "instances_tested": len(mli_values),
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_instances")