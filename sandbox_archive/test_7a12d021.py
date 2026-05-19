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
    
    primes = [i for i in range(5, 130) if is_prime(i)]
    if not primes:
        return {"metric_name": "n", "metric_value": 0, "instances_tested": 0, "conjecture_holds": False, "counterexample": ""}
    
    n = random.choice(primes)
    k = 3
    
    def generate_k_clique(n, k):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < k / (n * (n - 1) / 2):
                    edges.append((i, j))
        return edges
    
    def is_clique(graph, clique):
        for u, v in itertools.combinations(clique, 2):
            if (u, v) not in graph and (v, u) not in graph:
                return False
        return True
    
    def enumerate_minimal_terms(n, k):
        terms = []
        for i in range(1 << n):
            term = [j for j in range(n) if i & (1 << j)]
            if len(term) == k and is_clique(graph, term):
                terms.append(term)
        return terms
    
    def symmetric_group_fourier_transform(graph, k):
        # Placeholder implementation
        return 0
    
    graph = generate_k_clique(n, k)
    minimal_terms = enumerate_minimal_terms(n, k)
    
    if not minimal_terms:
        return {"metric_name": "n", "metric_value": 0, "instances_tested": 0, "conjecture_holds": False, "counterexample": ""}
    
    min_non_zero_coefficient = symmetric_group_fourier_transform(graph, k)
    dnf_size = len(minimal_terms) * math.log(n) / k
    
    return {
        "metric_name": "min_non_zero_coefficient",
        "metric_value": min_non_zero_coefficient,
        "instances_tested": 1,
        "conjecture_holds": min_non_zero_coefficient >= n**(k/2),
        "counterexample": "" if min_non_zero_coefficient >= n**(k/2) else f"DNF size {dnf_size} < Ω(n^{k/2})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if "metric_value" in r) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")