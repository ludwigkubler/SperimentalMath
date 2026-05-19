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
    
    def generate_dnf(n, k):
        clauses = set()
        for _ in range(k):
            clause = {random.randint(1, n) for _ in range(random.randint(1, n))}
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def is_k_clique(DNF, n, k):
        vertices = set(range(1, n + 1))
        for clause in DNF:
            if len(vertices.intersection(clause)) < k:
                return False
        return True
    
    def max_pairwise_disjoint_clauses(DNF):
        clauses = list(DNF)
        disjoint_clauses = []
        while clauses:
            selected_clause = clauses[0]
            disjoint_clauses.append(selected_clause)
            clauses = [c for c in clauses if not c.intersection(selected_clause)]
        return len(disjoint_clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        DNF = generate_dnf(n, k=5)
        if is_k_clique(DNF, n, 5):
            metric_value = max_pairwise_disjoint_clauses(DNF)
            conjecture_holds = metric_value >= n
            counterexample = "" if conjecture_holds else "k-CLIQUE instance"
        else:
            metric_value = max_pairwise_disjoint_clauses(DNF)
            conjecture_holds = metric_value <= math.log(n, 2)
            counterexample = "" if conjecture_holds else "random DNF"
        
        results.append({
            "metric_name": "max_disjoint_clauses",
            "metric_value": metric_value,
            "instances_tested": len(DNF),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(range(50, 80))
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")