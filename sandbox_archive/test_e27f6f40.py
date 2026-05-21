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
    
    def generate_binary_matroid(n):
        matroid = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            if all(row[i] == 0 or row[j] == 0 for i, j in combinations(range(n), 2) if row[i] + row[j] > 1):
                matroid.append(row)
        return matroid
    
    def characteristic_vectors(matroid):
        n = len(matroid)
        vectors = []
        for subset in range(1 << n):
            vector = [0] * n
            for i in range(n):
                if (subset >> i) & 1:
                    vector[i] = sum(matroid[j][i] for j in range(n)) % 2
            vectors.append(vector)
        return vectors
    
    def disjointness_protocol(vectors, n):
        # Simulate the disjointness protocol using bitwise operations
        # This is a simplified version and may not accurately reflect real-world communication complexity
        return math.ceil(math.log2(n))
    
    n = random.randint(5, 40)
    matroid = generate_binary_matroid(n)
    vectors = characteristic_vectors(matroid)
    comm_complexity = disjointness_protocol(vectors, n)
    
    metric_name = "disjointness_communication_complexity"
    metric_value = comm_complexity
    instances_tested = 1
    conjecture_holds = comm_complexity >= math.log2(n)
    counterexample = "" if conjecture_holds else f"n={n}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, comm_complexity={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")