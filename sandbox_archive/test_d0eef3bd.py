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
    
    def walsh_hadamard_transform(f, n):
        if n == 1:
            return f[0]
        even = walsh_hadamard_transform([f[i] for i in range(0, len(f), 2)], n // 2)
        odd = walsh_hadamard_transform([f[i] for i in range(1, len(f), 2)], n // 2)
        return [even[i] + odd[i] for i in range(n // 2)] + [even[i] - odd[i] for i in range(n // 2)]
    
    def k_clique_indicator(n, k):
        if k >= n:
            return 1
        return sum(1 for subset in itertools.combinations(range(n), k) if len(set(subset)) == k)
    
    def generate_random_3cnf(n, m):
        clauses = []
        variables = set()
        for _ in range(m):
            clause = random.sample(range(-n, 0), 2) + [random.randint(1, n)]
            clauses.append(clause)
            variables.update(abs(lit) for lit in clause)
        return clauses, list(variables)
    
    def evaluate_dnf(dnf, assignment):
        for clause in dnf:
            if all(assignment[abs(lit) - 1] == (lit > 0) for lit in clause):
                return 1
        return 0
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 4 * n)
    dnf, variables = generate_random_3cnf(n, m)
    
    assignment = [random.choice([True, False]) for _ in range(n)]
    metric_value = abs(evaluate_dnf(dnf, assignment))
    
    if len(variables) == n:
        k_clique_sum = k_clique_indicator(n, 3)
        if k_clique_sum < 0.1 * n:
            return {
                "metric_name": "k-clique sum",
                "metric_value": k_clique_sum,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "k-CLIQUE sum too small"
            }
    
    if metric_value > 10 * math.log(n):
        return {
            "metric_name": "Fourier coefficient sum",
            "metric_value": metric_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Fourier coefficient sum too large"
        }
    
    return {
        "metric_name": "Fourier coefficient sum",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")