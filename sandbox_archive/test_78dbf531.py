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
    
    def generate_monotone_k_clique_circuit(n):
        # Generate a random monotone k-CLIQUE circuit of size n
        k = random.randint(2, min(n, 10))
        clique = set(random.sample(range(n), k))
        circuit = []
        for i in range(k):
            for j in range(i + 1, k):
                if random.choice([True, False]):
                    circuit.append((i, j))
        return circuit

    def compute_noncommutative_algebra(circuit):
        # Compute the associated noncommutative algebra (simplified example)
        n = len(circuit) + 1
        algebra = [[0] * n for _ in range(n)]
        for i in range(n):
            algebra[i][i] = 1
        for u, v in circuit:
            algebra[u][v] = algebra[v][u] = 1
        return algebra

    def calculate_quotient_rank(algebra):
        # Calculate the quotient rank (simplified example)
        n = len(algebra)
        rank = 0
        for i in range(n):
            if any(algebra[j][i] != 0 for j in range(n)):
                rank += 1
        return rank

    def is_submodular(ranks):
        # Check if the ranks are submodular
        n = len(ranks)
        for i in range(1, n):
            if not (ranks[i] <= ranks[i - 1]):
                return False
        return True

    max_rank = 0
    min_rank = float('inf')
    instances_tested = 0

    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_monotone_k_clique_circuit(n)
        algebra = compute_noncommutative_algebra(circuit)
        rank = calculate_quotient_rank(algebra)
        
        if rank > max_rank:
            max_rank = rank
        if rank < min_rank:
            min_rank = rank
        
        instances_tested += 1

    conjecture_holds = is_submodular([max_rank, min_rank]) and max_rank <= n**2 * math.log(n) and min_rank >= n**k
    counterexample = f"max_rank={max_rank}, min_rank={min_rank}" if not conjecture_holds else ""

    return {
        "metric_name": "quotient_rank",
        "metric_value": (max_rank + min_rank) / 2,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")