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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [i for i in range(5, 40) if is_prime(i)]
    
    def generate_dnf(n):
        terms = []
        for _ in range(random.randint(2, 5)):
            term = set()
            for j in range(n):
                if random.random() < 0.3:
                    term.add(j)
            terms.append(term)
        return terms
    
    def compute_mu(dnf, k):
        n = len(dnf[0])
        target_cliques = []
        for i in range(1 << n):
            clique = set()
            for j in range(n):
                if i & (1 << j):
                    clique.add(j)
            if len(clique) == k and all(term.issubset(clique) for term in dnf):
                target_cliques.append(clique)
        
        min_terms = float('inf')
        for _ in range(100):  # Randomized search
            selected_terms = random.sample(dnf, len(dnf))
            covered = set()
            for term in selected_terms:
                covered.update(term)
            if all(len(covered & clique) > 0 for clique in target_cliques):
                min_terms = min(min_terms, len(selected_terms))
        return min_terms
    
    def k_clique(n, k):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    results = []
    for n in primes:
        dnf = generate_dnf(n)
        mu = compute_mu(dnf, k=2)  # Example for k=2
        results.append({"n": n, "mu": mu})
    
    mean_mu = sum(result["mu"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["mu"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["mu"] >= n) / len(results)
    
    return {
        "metric_name": "submodular_measure",
        "metric_value": mean_mu,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, mu={results[0]['mu']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_mu = sum(result["metric_value"] for result in results) / len(results)
    std_mu = math.sqrt(sum((result["metric_value"] - mean_mu) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, mu={results[0]['mu']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")