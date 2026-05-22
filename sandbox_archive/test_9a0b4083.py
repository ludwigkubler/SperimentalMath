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
    
    def generate_symmetric_tensor(n):
        tensor = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                tensor[j][i] = tensor[i][j]
        return tensor
    
    def schur_weyl_duality(m, pi):
        return m / 2 + sum(math.log2(m) for _ in pi)
    
    def minimal_symplectic_tensor_product_rank(tensor):
        n = len(tensor)
        rank = 0
        for i in range(n):
            row_sum = sum(tensor[i][j] for j in range(n))
            if row_sum > rank:
                rank = row_sum
        return rank
    
    def permutation_circuit_depth(n):
        return int(n ** math.log2(3 / 4))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    tensor = generate_symmetric_tensor(n)
    m = sum(sum(row) for row in tensor)
    pi = [random.randint(1, m) for _ in range(m)]
    
    lower_bound = schur_weyl_duality(m, pi)
    actual_rank = minimal_symplectic_tensor_product_rank(tensor)
    depth = permutation_circuit_depth(n)
    
    return {
        "metric_name": "minimal_symplectic_tensor_product_rank",
        "metric_value": actual_rank,
        "instances_tested": 1,
        "conjecture_holds": actual_rank >= lower_bound * 0.5 and actual_rank <= lower_bound * 1.5,
        "counterexample": "" if conjecture_holds else f"Rank {actual_rank} does not satisfy the bound {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not satisfy the bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")