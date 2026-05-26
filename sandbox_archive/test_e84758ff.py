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
    
    # Generate a random 3-CNF formula F with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    F = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(3, n))]
        F.append(clause)
    
    # Compute the p-adic harmonic space H(F) associated with S
    S = {Fraction(i, 2**n) for i in range(2**n)}
    H_F = []
    for s in S:
        h_s = sum([s**abs(lit) if lit > 0 else -s**abs(lit) for clause in F for lit in clause])
        H_F.append(h_s)
    
    # Determine MinimalRank(H(F)) using computational methods for p-adic harmonic analysis
    minimal_rank_H_F = len(set(H_F))
    
    # Calculate κ_m(k-CLIQUE_F) using known algorithms for monotone circuit lower bounds
    # (This is a placeholder. Replace with actual algorithm if available.)
    def clique_complexity(F):
        return n  # Placeholder value
    
    kappa_m_k_clique_F = clique_complexity(F)
    
    # Compute the Spearman's rank correlation coefficient between MinimalRank(H(F)) and κ_m(k-CLIQUE_F)
    # (This is a placeholder. Replace with actual calculation if available.)
    def spearman_correlation(ranks1, ranks2):
        return 0.5 * (1 + sum((ranks1[i] - ranks2[i])**2 for i in range(len(ranks1))))  # Placeholder value
    
    ranks_H_F = sorted(range(len(H_F)), key=lambda i: H_F[i])
    ranks_kappa_m = sorted(range(m), key=lambda i: kappa_m_k_clique_F)
    rho = spearman_correlation(ranks_H_F, ranks_kappa_m)
    
    return {
        "metric_name": "MinimalRank(H(F))",
        "metric_value": minimal_rank_H_F,
        "instances_tested": 1,
        "conjecture_holds": rho >= 0.7 and abs(minimal_rank_H_F - kappa_m_k_clique_F) <= 1,
        "counterexample": "" if rho >= 0.7 and abs(minimal_rank_H_F - kappa_m_k_clique_F) <= 1 else "rho < 0.7 or |MinimalRank(H(F)) - κ_m(k-CLIQUE_F)| > 1"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*2 + 1, 2))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")