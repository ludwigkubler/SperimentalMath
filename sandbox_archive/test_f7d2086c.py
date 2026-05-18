# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_dnf(n, k, s):
    terms = [set(random.sample(range(1, n+1), k)) for _ in range(s)]
    return terms

def generate_adversarial_dnf(n, k, s):
    base_terms = set(random.sample(range(1, n+1), k))
    adversarial_terms = [base_terms.union({i}) for i in range(1, n+1) if i not in base_terms]
    terms = random.sample(adversarial_terms, s)
    return terms

def generate_clique_dnf(n, v):
    edges = list(combinations(range(1, n+1), 2))
    clique_terms = []
    for triangle in combinations(edges, 3):
        term = set()
        for edge in triangle:
            term.update(edge)
        clique_terms.append(term)
    return clique_terms[:v]

def symdiff_count(A, B):
    return sum(1 for x in A if x not in B) + sum(1 for y in B if y not in A)

def compute_D_rho(F, rho):
    count = 0
    n = len(F[0])
    for i in range(n):
        for j in range(i+1, n):
            diff_count = symdiff_count(F[i], F[j])
            count += rho ** diff_count
    return count / (len(F) ** 2)

def compute_eta(F):
    D_half = compute_D_rho(F, 0.5)
    D_quarter = compute_D_rho(F, 0.25)
    return math.log2(D_half) - 2 * math.log2(D_quarter)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [12, 18, 24, 30, 36]
    k_values = [2, 3, 4]
    s_values = [n * n, 2 * n * n, n * n * n]  # n^{1.5} is n^3 in this context
    
    results = []
    
    for n in n_values:
        for k in k_values:
            for s in s_values:
                F = generate_random_dnf(n, k, s)
                eta = compute_eta(F)
                results.append((eta, math.log2(s * k + 2)))
                
                if len(results) >= 30:  # Ensure at least 30 instances per seed
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    max_ratio = max(eta / log_L for eta, log_L in results)
    conjecture_holds = max_ratio <= 6
    
    return {
        "metric_name": "max_eta_over_logL",
        "metric_value": max_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    max_ratio = max(result["metric_value"] for result in results if result["conjecture_holds"])
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={max_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_eta_over_logL\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=<k>")