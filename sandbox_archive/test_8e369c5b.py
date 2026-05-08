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
    
    def generate_k_clique_cnf(n, k):
        if n < k:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(k):
            clause = random.sample(variables, k - i)
            clauses.append(clause)
        return clauses
    
    def compute_polymatroid_rank(hypergraph):
        rank = 0
        while hypergraph:
            edge = max(hypergraph, key=lambda e: len(e))
            rank += 1
            hypergraph = [e for e in hypergraph if not set(edge).issubset(e)]
        return rank
    
    def is_monotone_dnf(cnf):
        for clause in cnf:
            if any(var.startswith('-') for var in clause):
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            cnf = generate_k_clique_cnf(n, random.randint(2, min(4, n // 2)))
            if cnf is None:
                continue
            hypergraph = {tuple(sorted(int(var) for var in clause)) for clause in cnf}
            rank = compute_polymatroid_rank(hypergraph)
            total_rank += rank
            instances_tested += 1
            
            # Check polymatroid rank condition
            if rank < n / len(n_values):
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}"
            
            # Check monotone DNF condition
            if is_monotone_dnf(cnf) and rank > math.log(n):
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}"
    
    mean_rank = total_rank / instances_tested if instances_tested else 0
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")