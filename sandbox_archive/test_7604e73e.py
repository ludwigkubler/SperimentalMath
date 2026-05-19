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
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            clauses.append(clause)
        return clauses
    
    def is_k_clique(clauses, n):
        for i in range(n):
            for j in range(i + 1, n):
                if not any((i+1 in clause and j+1 in clause) for clause in clauses):
                    return False
        return True
    
    def max_disjoint_clauses(clauses):
        disjoint = []
        for clause in clauses:
            if all(len(set(clause).intersection(d)) == 0 for d in disjoint):
                disjoint.append(clause)
        return len(disjoint)
    
    n, k = random.randint(5, 40), 5
    dnf = generate_dnf(n, k)
    
    if is_k_clique(dnf, n):
        metric_value = max_disjoint_clauses(dnf)
        conjecture_holds = metric_value >= n
        counterexample = "" if conjecture_holds else "Non-k-clique DNF found"
    else:
        metric_value = max_disjoint_clauses(dnf)
        conjecture_holds = metric_value <= math.log(n, 2)
        counterexample = "" if conjecture_holds else "Non-k-clique DNF found"
    
    return {
        "metric_name": "disjoint_clauses",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-k-clique DNF found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")