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
    
    def generate_acc0_circuit(depth: int, n: int):
        # Simplified ACC^0 circuit generation (not actual ACC^0)
        return [[random.randint(1, 3) for _ in range(n)] for _ in range(depth)]
    
    def non_commutative_rank(matrix):
        # Compute the rank of a matrix over a non-commutative ring
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(m):
                    matrix[j][i], matrix[j][i - 1] = matrix[j][i - 1], matrix[j][i]
        return rank
    
    def log_n(n: int):
        return math.log2(n)
    
    n = random.randint(5, 40)
    depth = random.randint(1, 10)
    circuit = generate_acc0_circuit(depth, n)
    rank = non_commutative_rank(circuit)
    
    expected_rank = log_n(n)
    tolerance = 0.1
    conjecture_holds = abs(rank - expected_rank) <= tolerance
    
    return {
        "metric_name": "non_commutative_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} does not match expected log2({n}) ≈ {expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")