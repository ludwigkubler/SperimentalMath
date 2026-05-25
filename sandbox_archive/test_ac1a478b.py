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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def negation_cayley_representation(k_cnf):
        n = len(k_cnf[0])
        cayley_rep = []
        for clause in k_cnf:
            rep = [0] * (n + 1)
            for lit in clause:
                if lit > 0:
                    rep[lit - 1] += 1
                else:
                    rep[-lit - 1] -= 1
            cayley_rep.append(rep)
        return cayley_rep
    
    def tropicalize(cayley_rep):
        n = len(cayley_rep[0])
        tropicalized = []
        for row in cayley_rep:
            tropicalized_row = [max(row[i], -row[n-i-1]) for i in range(n)]
            tropicalized.append(tropicalized_row)
        return tropicalized
    
    def minimal_rank(tropicalized):
        n = len(tropicalized[0])
        rank = 0
        for row in tropicalized:
            if any(x != 0 for x in row):
                rank += 1
        return rank
    
    def monotone_k_clique_circuit_size(n, k):
        # Simplified approximation based on known results
        return 2 ** (n ** (1/2 - k))
    
    n = random.randint(5, 40)
    k_cnf = generate_k_cnf(n)
    cayley_rep = negation_cayley_representation(k_cnf)
    tropicalized = tropicalize(cayley_rep)
    rank = minimal_rank(tropicalized)
    circuit_size = monotone_k_clique_circuit_size(n, 2)  # Assuming k=2 for simplicity
    
    expected_rank = n ** (1/2 - 2) * (1 + random.random() / 10)  # ±10% variation
    within_range = abs(rank - expected_rank) <= 0.1 * expected_rank
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": within_range and circuit_size <= 2 ** (n ** (1/2 - 2)),
        "counterexample": "" if within_range else f"Rank {rank} not within ±10% of {expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")