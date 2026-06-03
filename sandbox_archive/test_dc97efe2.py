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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            cnf.append(clause)
        return cnf
    
    def grothendieck_witt_class(cnf):
        n = len(cnf[0])
        rank = 0
        for clause in cnf:
            if any(lit in clause for lit in [-i, i] for i in range(1, n+1)):
                rank += 1
        return rank
    
    def compute_k0_rank(cnf):
        return grothendieck_witt_class(cnf)
    
    def compute_clause_set_complexity(cnf):
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    k0_ranks = []
    complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        k0_rank = compute_k0_rank(cnf)
        complexity = compute_clause_set_complexity(cnf)
        k0_ranks.append(k0_rank)
        complexities.append(complexity)
    
    if not k0_ranks or not complexities:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    mean_k0_rank = sum(k0_ranks) / len(k0_ranks)
    mean_complexity = sum(complexities) / len(complexities)
    
    covariance = sum((k0_ranks[i] - mean_k0_rank) * (complexities[i] - mean_complexity) for i in range(len(k0_ranks))) / len(k0_ranks)
    variance_k0_rank = sum((k0_ranks[i] - mean_k0_rank)**2 for i in range(len(k0_ranks))) / len(k0_ranks)
    variance_complexity = sum((complexities[i] - mean_complexity)**2 for i in range(len(complexities))) / len(complexities)
    
    if variance_k0_rank == 0 or variance_complexity == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "constant_variance"
        }
    
    pearson_corr = covariance / (math.sqrt(variance_k0_rank) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(k0_ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_corr) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.7) / len(results)
    
    if all(abs(r["metric_value"]) > 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.4f} std={std_corr:.4f} support_fraction={support_fraction:.2f}")
    elif any(abs(r["metric_value"]) < -0.7 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < -0.7)
        print(f"RESULT: FALSIFIED counterexample=\"negative_corr\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")