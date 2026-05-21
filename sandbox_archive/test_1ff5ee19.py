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
    
    def sturm_sequence(poly):
        if not poly:
            return []
        seq = [poly]
        while True:
            lead_coeff = seq[-1][-1]
            diff = [-c * i for i, c in enumerate(seq[-1])]
            diff.pop(0)
            if not diff:
                break
            seq.append(diff)
        return seq
    
    def count_real_roots(poly):
        seq = sturm_sequence(poly)
        sign_changes_pos = sum(
            (seq[i][-1] > 0) != (seq[i+1][-1] > 0) for i in range(len(seq)-1)
        )
        sign_changes_neg = sum(
            (-seq[i][-1] > 0) != (-seq[i+1][-1] > 0) for i in range(len(seq)-1)
        )
        return sign_changes_pos - sign_changes_neg
    
    def generate_k_clique(n, k):
        if k >= n:
            return []
        vertices = list(range(n))
        clique = random.sample(vertices, k)
        remaining = [v for v in vertices if v not in clique]
        edges = []
        for i in range(k):
            for j in range(i+1, k):
                edges.append((clique[i], clique[j]))
        return clique, edges
    
    def generate_random_dnf(n, m):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def real_stable_polynomial(clauses):
        poly = [1]
        for clause in clauses:
            monomial = 1
            for var in clause:
                monomial *= (var + 1) * (-var - 1)
            poly += [monomial] + [0] * len(poly[:-1])
        return poly
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(2, min(n-1, 5))
        clique_clauses = generate_k_clique(n, k)
        dnf_clauses = generate_random_dnf(n, int(n**1.5))
        
        clique_poly = real_stable_polynomial(clique_clauses)
        dnf_poly = real_stable_polynomial(dnf_clauses)
        
        clique_roots = count_real_roots(clique_poly)
        dnf_roots = count_real_roots(dnf_poly)
        
        results.append({
            "n": n,
            "k": k,
            "clique_roots": clique_roots,
            "dnf_roots": dnf_roots
        })
    
    total_clique_roots = sum(res["clique_roots"] for res in results)
    total_dnf_roots = sum(res["dnf_roots"] for res in results)
    
    mean_clique_roots = total_clique_roots / len(results)
    mean_dnf_roots = total_dnf_roots / len(results)
    
    conjecture_holds = all(mean_clique_roots >= n/10 for n in n_values)
    counterexample = "" if conjecture_holds else "k-CLIQUE root count < n/10"
    
    return {
        "metric_name": "mean_real_roots",
        "metric_value": mean_dnf_roots,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"k-CLIQUE root count < n/10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction too low")