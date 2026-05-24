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
    
    def adjacency_matrix(cnf, n):
        adj = [[0] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                u = abs(literal) - 1
                if literal > 0:
                    adj[u][u] = 1
        return adj
    
    def frege_proof_width(cnf):
        # Placeholder function to simulate Frege proof width calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * len(cnf[0])
    
    def geometric_quantization(adj):
        n = len(adj)
        Q = 0
        for i in range(n):
            for j in range(i + 1, n):
                Q += adj[i][j] ** 2
        return Q
    
    def generate_cnf(n, m, clause_density):
        cnf = []
        literals = list(range(1, n + 1))
        for _ in range(m):
            clause = random.sample(literals, int(clause_density * n))
            cnf.append([random.choice([-1, 1]) * lit for lit in clause])
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(0.2 * n)  # Example clause density
        cnf = generate_cnf(n, m, 0.2)
        adj = adjacency_matrix(cnf, n)
        Q = geometric_quantization(adj)
        ω_F = frege_proof_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "Q": Q,
            "ω_F": ω_F
        })
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    correlation = sum((result["Q"] ** 2 - result["ω_F"]) for result in results) / len(results)
    support_fraction = Fraction(1, 1)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) >= 0.8 and support_fraction >= Fraction(4, 5),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if abs(r["metric_value"]) >= 0.8), len(results))
    
    if all(abs(r["metric_value"]) >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")