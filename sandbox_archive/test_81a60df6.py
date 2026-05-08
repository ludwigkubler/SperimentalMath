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
    
    def generate_monotone_dnf(n, size):
        terms = []
        for _ in range(size):
            term = [random.choice([0, 1]) for _ in range(n)]
            if all(term[i] == 0 or term[j] == 0 for i, j in combinations(range(n), 2)):
                terms.append(term)
        return terms
    
    def is_independent_set(S, dnf_formula):
        n = len(dnf_formula[0])
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for u, v in edges:
            if any(S[i] == S[j] == 1 for term in dnf_formula if term[u] == term[v]):
                return False
        return True
    
    def compute_mu(dnf_formula):
        max_disjoint_terms = 0
        n = len(dnf_formula[0])
        for i in range(1 << n):
            S = [i >> j & 1 for j in range(n)]
            if is_independent_set(S, dnf_formula):
                max_disjoint_terms += 1
        return max_disjoint_terms
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size = int(n**2)
        dnf_formula = generate_monotone_dnf(n, size)
        mu_f = compute_mu(dnf_formula)
        results.append({"n": n, "size": size, "mu_f": mu_f})
    
    mean_mu_f = sum(result["mu_f"] for result in results) / len(results)
    std_mu_f = math.sqrt(sum((result["mu_f"] - mean_mu_f)**2 for result in results) / len(results))
    support_fraction = all(mu_f <= math.log(n) for n, _, mu_f in results if n < 10)
    
    return {
        "metric_name": "μ(f)",
        "metric_value": mean_mu_f,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else f"n={results[-1]['n']}, mu_f={results[-1]['mu_f']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mu_f = sum(result["metric_value"] for result in results) / len(results)
    std_mu_f = math.sqrt(sum((result["metric_value"] - mean_mu_f)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results if "counterexample" not in result)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_mu_f} std={std_mu_f} support_fraction=1.0")
    elif any("counterexample" in result for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")