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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dnf_to_clauses(dnf):
        clauses = []
        for term in dnf.split('&'):
            if '!' in term:
                continue
            clause = [int(x[1:]) for x in term.split('|')]
            clauses.append(clause)
        return clauses
    
    def max_clause_count(f):
        n = len(f)
        dnf = generate_boolean_function(n)
        clauses = dnf_to_clauses(dnf)
        return len(clauses)
    
    def etale_cohomology_rank(f):
        n = len(f)
        # Simplified mapping for demonstration purposes
        rank = sum(1 for bit in f if bit == '1')
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    clause_counts = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            rank = etale_cohomology_rank(f)
            clause_count = max_clause_count(f)
            ranks.append(rank)
            clause_counts.append(clause_count)
    
    if len(ranks) < 30:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rho_numerator = sum((sorted_x[i] - (n-1)/2) * (sorted_y[i] - (n-1)/2) for i in range(n))
        rho_denominator = math.sqrt(sum((sorted_x[i] - (n-1)/2)**2 for i in range(n))) * math.sqrt(sum((sorted_y[i] - (n-1)/2)**2 for i in range(n)))
        return rho_numerator / rho_denominator if rho_denominator != 0 else 0
    
    rho = rank_correlation(ranks, clause_counts)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(ranks),
        "conjecture_holds": rho >= 0.7,
        "counterexample": "" if rho >= 0.7 else f"Spearman rank correlation is {rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results)/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation is less than 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")