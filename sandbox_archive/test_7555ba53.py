# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def delone_set_geometry(clauses):
        n = len(clauses[0])
        points = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for var in clause:
                if abs(var) <= n:
                    points[-var - 1][-var - 1] += 1
        return points
    
    def ac0_k_distance_circuit_size(clauses):
        m = len(clauses)
        # Simplified heuristic: size is proportional to the number of clauses
        return m * 2
    
    n = random.randint(5, 40)
    m = random.randint(n + 1, n * (n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if len(set(clause)) == 2:
            clauses.append(clause)
    
    geometry = delone_set_geometry(clauses)
    rank = sum(sum(row) for row in geometry)
    circuit_size = ac0_k_distance_circuit_size(clauses)
    
    return {
        "metric_name": "rank_vs_circuit_size",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= circuit_size ** 2 and circuit_size <= m,
        "counterexample": "" if rank <= circuit_size ** 2 and circuit_size <= m else f"Rank {rank} > Circuit Size^2 ({circuit_size**2}), Circuit Size {circuit_size} > Clauses {m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")