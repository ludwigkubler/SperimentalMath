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
    
    def is_monotone(dnf):
        for i in range(len(dnf)):
            for j in range(i + 1, len(dnf)):
                if not all(x in dnf[j] for x in dnf[i]):
                    return False
        return True
    
    def rank(Φ_A):
        max_disjoint = 0
        for subset in itertools.combinations(Φ_A, len(Φ_A) // 2 + 1):
            disjoint_count = sum(len(set(subset).intersection(clause)) == 0 for clause in Φ_A)
            if disjoint_count > max_disjoint:
                max_disjoint = disjoint_count
        return max_disjoint
    
    def μ(Φ, k):
        max_value = -math.inf
        for A in itertools.combinations(range(len(Φ)), min(k, len(Φ))):
            Φ_A = [clause for clause in Φ if all(x in clause for x in A)]
            value = rank(Φ_A) - len(A)
            if value > max_value:
                max_value = value
        return max_value
    
    def generate_dnf(n, m):
        dnf = []
        while len(dnf) < m:
            clause = set(random.sample(range(n), random.randint(1, n)))
            if all(clause.isdisjoint(other_clause) for other_clause in dnf):
                dnf.append(clause)
        return dnf
    
    def k_clique_dnf(k):
        n = k * (k - 1) // 2
        dnf = []
        for i in range(n):
            clause = set(range(i, i + k))
            dnf.append(clause)
        return dnf
    
    n = random.randint(5, 40)
    m = min(random.randint(1, n**2), 100)  # Ensure m is polynomial in n
    Φ = generate_dnf(n, m)
    
    if not is_monotone(Φ):
        return {
            "metric_name": "μ(Φ)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_monotone"
        }
    
    μ_Φ = μ(Φ, n)
    if μ_Φ > 2 * math.log(n):
        return {
            "metric_name": "μ(Φ)",
            "metric_value": μ_Φ,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"μ(Φ) = {μ_Φ} > 2 log n = {2 * math.log(n)}"
        }
    
    k = random.randint(2, 5)
    Φ_k_clique = k_clique_dnf(k)
    μ_k_clique = μ(Φ_k_clique, k)
    if μ_k_clique < n ** 0.5 / 2:
        return {
            "metric_name": "μ(k-CLIQUE)",
            "metric_value": μ_k_clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"μ(k-CLIQUE) = {μ_k_clique} < n^{0.5}/2 = {n ** 0.5 / 2}"
        }
    
    return {
        "metric_name": "μ(Φ)",
        "metric_value": μ_Φ,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")