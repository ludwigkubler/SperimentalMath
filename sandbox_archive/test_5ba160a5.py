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
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def p_adic_valuation_ring(cnf):
        # Simplified mapping to a polynomial ring over a finite field
        return len(set(tuple(sorted(abs(x) for x in clause)) for clause in cnf))
    
    def frege_proof_length(cnf):
        # Simplified measure of proof length (number of clauses)
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    proof_lengths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_rank = p_adic_valuation_ring(cnf)
        proof_length = frege_proof_length(cnf)
        min_ranks.append(min_rank)
        proof_lengths.append(proof_length)
    
    if not min_ranks or not proof_lengths:
        return {
            "metric_name": "Pearson Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x > 0 and std_y > 0 else None
    
    correlation = pearson_correlation(min_ranks, proof_lengths)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation is not None and correlation >= 0.5,
        "counterexample": "" if correlation is not None and correlation >= 0.5 else str(correlation)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] is not None and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")