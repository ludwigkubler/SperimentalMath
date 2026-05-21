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
    
    def is_k_clique_computing(dnf):
        n = len(dnf[0])
        k = sum(1 for term in dnf if len(term) == k)
        M = [[0] * n for _ in range(k)]
        
        for i, term in enumerate(dnf):
            for v in term:
                M[i][v] += 1
        
        def fft(a):
            n = len(a)
            if n <= 1: return a
            even = fft(a[::2])
            odd = fft(a[1::2])
            T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
            return [even[k] + T[k] for k in range(n // 2)] + [even[k] - T[k] for k in range(n // 2)]
        
        M_fft = [fft(row) for row in M]
        mu = sum(1 for col in zip(*M_fft) if any(abs(entry) > 1e-9 for entry in col))
        return mu >= n // 2
    
    def generate_k_clique_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        clique_edges = random.sample(edges, k)
        dnf = []
        for edge_set in itertools.combinations(clique_edges, k - 2):
            term = [edge[0] for edge in edge_set]
            for v in range(n):
                if v not in {e[0] for e in edge_set}:
                    term.append(v)
            dnf.append(term)
        return dnf
    
    def generate_random_dnf(n, k):
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random_edges = random.sample(edges, k * 2)
        dnf = []
        for edge_set in itertools.combinations(random_edges, k - 2):
            term = [edge[0] for edge in edge_set]
            for v in range(n):
                if v not in {e[0] for e in edge_set}:
                    term.append(v)
            dnf.append(term)
        return dnf
    
    n_values = [6, 8, 10, 12, 12, 16, 20]
    k_values = [3, 3, 3, 3, 4, 4, 4]
    
    results = []
    for n, k in zip(n_values, k_values):
        if n < 2 * k or k < 3:
            continue
        
        canonical_dnf = generate_k_clique_dnf(n, k)
        padded_dnf = canonical_dnf + generate_random_dnf(n, k)
        
        mu_canonical = is_k_clique_computing(canonical_dnf)
        mu_padded = is_k_clique_computing(padded_dnf)
        
        results.append({
            "n": n,
            "k": k,
            "mu_canonical": mu_canonical,
            "mu_padded": mu_padded
        })
    
    mean_mu_canonical = sum(result["mu_canonical"] for result in results) / len(results)
    mean_mu_padded = sum(result["mu_padded"] for result in results) / len(results)
    
    support_fraction = sum(1 for result in results if result["mu_canonical"]) / len(results)
    
    return {
        "metric_name": "Cyclic Fourier Spread",
        "metric_value": mean_mu_canonical,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"n={results[0]['n']}, k={results[0]['k']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_mu_canonical = sum(result["mu_canonical"] for result in results) / len(results)
    mean_mu_padded = sum(result["mu_padded"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["mu_canonical"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_mu_canonical} std=0 support_fraction={support_fraction}")
    elif any(not result["mu_canonical"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["mu_canonical"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, k={results[0]['k']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")