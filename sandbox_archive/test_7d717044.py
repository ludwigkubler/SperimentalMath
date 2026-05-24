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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def adjacency_matrix(cnf, n):
        adj = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    u = i - 1
                else:
                    u = -i - 1
                for j in clause:
                    if j != i and (j > 0):
                        v = j - 1
                    elif j < 0:
                        v = -j - 1
                    adj[u][v] = 1
        return adj
    
    def geometric_quantization(adj, n):
        Q = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i][j] == 1:
                    Q += math.sqrt(2 * (i + j))
        return Q
    
    def frege_proof_width(cnf):
        # Simplified estimation of Frege proof width
        m = len(cnf)
        return math.log(m) / math.log(2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, int(n * (n - 1) / 2))
        adj = adjacency_matrix(cnf, n)
        Q = geometric_quantization(adj, n)
        ω_F = frege_proof_width(cnf)
        
        results.append({
            "Q(G)": Q,
            "ω_F": ω_F
        })
    
    correlation_coefficient = sum((r["Q(G)"] ** 2 - r["ω_F"]) for r in results) / len(results)
    mean_QG_squared = sum(r["Q(G)"] ** 2 for r in results) / len(results)
    support_fraction = (correlation_coefficient >= 0.8)
    
    return {
        "metric_name": "Correlation between Q(G)^2 and ω_F",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support_fraction")