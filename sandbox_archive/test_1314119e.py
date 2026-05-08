# auto-injected by SEC sandbox
import math
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
from itertools import combinations

def binomial(n, k):
    if k > n:
        return 0
    res = 1
    for i in range(k):
        res *= (n - i)
        res //= (i + 1)
    return res

def power_set(s):
    result = []
    for r in range(len(s) + 1):
        for subset in combinations(s, r):
            result.append(subset)
    return result

def euler_characteristic(Δ):
    if not Δ:
        return -1
    n = len(Δ[0])
    layers = [[] for _ in range(n + 1)]
    for face in Δ:
        layers[len(face)].append(face)
    
    chi = -1
    sign = 1
    for layer in layers:
        chi += sign * len(layer)
        sign *= -1
    return chi

def canonical_k_clique_dnf(n, k):
    edges = set()
    for clique in combinations(range(n), k):
        for i in range(k):
            for j in range(i + 1, k):
                edges.add((clique[i], clique[j]))
    return edges

def sample_random_k_vertex_subsets(n, k, s):
    vertices = list(range(n))
    subsets = []
    for _ in range(s):
        subset = random.sample(vertices, k)
        subsets.append(subset)
    return subsets

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    n_values = [8, 12, 16, 20, 24, 28, 32]
    k_values = [3, 4]
    
    for n in n_values:
        for k in k_values:
            # (a) Compute μ(f*)
            f_star_edges = canonical_k_clique_dnf(n, k)
            f_star_complex = power_set(f_star_edges)
            mu_f_star = euler_characteristic(f_star_complex)
            
            if k == 3 and n == 8:
                assert mu_f_star == -1 + binomial(28, 2) - binomial(8, 3), "Sanity check failed for (n=8, k=3)"
            
            # (b) Compute μ(g)
            s = n
            g_edges = sample_random_k_vertex_subsets(n, k, s)
            g_complex = power_set(g_edges)
            mu_g = euler_characteristic(g_complex)
            
            results.append({
                "n": n,
                "k": k,
                "mu_f_star": mu_f_star,
                "mu_g": mu_g
            })
    
    # Verify (a) and (b)
    valid_a = all(result["mu_f_star"] >= result["n"]**result["k"] / (2 * result["k"] * math.factorial(result["k"])) for result in results if result["k"] == 3 or result["k"] == 4)
    valid_b = all(result["mu_g"] <= 4 * result["s"] * 2**(result["k"]*(result["k"]-1)//2) for result in results)
    
    # Compute μ(f*)/median μ(g)
    mu_f_star_values = [result["mu_f_star"] for result in results]
    median_mu_g = sorted([result["mu_g"] for result in results])[len(results) // 2]
    gap_growth_rate = max(mu_f_star / median_mu_g for mu_f_star in mu_f_star_values)
    
    # Check if the conjecture holds
    conjecture_holds = valid_a and valid_b and gap_growth_rate >= n**(k-1)/8
    
    return {
        "metric_name": "mu_gap_growth_rate",
        "metric_value": gap_growth_rate,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mu_gap_growth_rates = [r["metric_value"] for r in results]
    mean_mu_gap_growth_rate = sum(mu_gap_growth_rates) / len(mu_gap_growth_rates)
    std_mu_gap_growth_rate = (sum((x - mean_mu_gap_growth_rate)**2 for x in mu_gap_growth_rates) / len(mu_gap_growth_rates))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu_gap_growth_rate} std={std_mu_gap_growth_rate} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or refute the conjecture")