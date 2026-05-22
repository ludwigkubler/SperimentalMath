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
    
    def generate_monotone_kclique_circuit(k, n):
        if k > n or n < 1:
            return []
        circuit = []
        for i in range(n):
            if len(circuit) >= k:
                break
            if random.choice([True, False]):
                circuit.append(i)
        return circuit
    
    def compute_noncommutative_algebra(circuit):
        n = len(circuit)
        algebra = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in range(u + 1, n):
                if (u in circuit and v in circuit) or (u not in circuit and v not in circuit):
                    algebra[u][v] = algebra[v][u] = 1
        return algebra
    
    def compute_quotient_rank(algebra):
        n = len(algebra)
        rank = 0
        for i in range(n):
            row_sum = sum(algebra[i])
            if row_sum > 0:
                rank += 1
        return rank
    
    def is_submodular(ranks, n):
        for k in range(2, n + 1):
            for i in range(k - 1):
                for j in range(i + 1, k):
                    if ranks[j] < ranks[i] + ranks[k - 1] - ranks[j]:
                        return False
        return True
    
    def is_within_bounds(ranks, n):
        for rank in ranks:
            if rank > n**2 * math.log(n) or rank < n**n:
                return False
        return True
    
    max_n = 40
    instances_tested = 0
    submodular_ranks = []
    
    for n in range(5, max_n + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            circuit = generate_monotone_kclique_circuit(k=2, n=n)
            if not circuit:
                continue
            algebra = compute_noncommutative_algebra(circuit)
            rank = compute_quotient_rank(algebra)
            submodular_ranks.append(rank)
            instances_tested += 1
    
    conjecture_holds = is_submodular(submodular_ranks, max_n) and is_within_bounds(submodular_ranks, max_n)
    counterexample = "" if conjecture_holds else "submodularity or bounds violated"
    
    return {
        "metric_name": "Quotient Rank",
        "metric_value": sum(submodular_ranks) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")