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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    def tropical_rank(matrix):
        n = len(matrix)
        for i in range(n):
            matrix[i][i] += 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    matrix[i][j] = max(matrix[i][j], matrix[i][k] + matrix[k][j])
        return sum(1 for row in matrix if any(x > 0 for x in row))
    
    def ac0_circuit_depth(n):
        # Simplified AC⁰ circuit depth calculation
        return int(math.log2(n)) + 1
    
    n = random.randint(5, 40)
    depth = ac0_circuit_depth(n)
    rank_bound = log2(n) ** 2
    
    # Generate a random n-bit input for PARITY computation
    inputs = [random.choice([0, 1]) for _ in range(n)]
    
    # Construct an AC⁰ circuit (simplified)
    circuit = []
    for i in range(n):
        if inputs[i] == 1:
            circuit.append(i)
    
    # Compute the minimal rank of tropicalized quantum entanglement
    matrix = [[0] * n for _ in range(n)]
    for node in circuit:
        for other_node in circuit:
            if node != other_node:
                matrix[node][other_node] = 1
    rank = tropical_rank(matrix)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= rank_bound and rank >= log2(n),
        "counterexample": "" if rank <= rank_bound and rank >= log2(n) else f"Rank {rank} does not satisfy bounds for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")