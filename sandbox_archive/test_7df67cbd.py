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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def frege_proof_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = float('inf')
        for i in range(1, n):
            left = f[:i]
            right = f[i:]
            if all(left[j] == right[j] for j in range(i)):
                depth = min(depth, frege_proof_depth(left) + frege_proof_depth(right))
        return depth
    
    def geometric_quantization_rank(f):
        n = len(f)
        state = [f.count(0), f.count(1)]
        rank = 0
        while sum(state) > 1:
            if state[0] > state[1]:
                state[0] -= 1
                state[1] += 1
            else:
                state[0] += 1
                state[1] -= 1
            rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    depth = frege_proof_depth(f)
    rank = geometric_quantization_rank(f)
    
    return {
        "metric_name": "GQR vs Frege Depth",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= depth,
        "counterexample": "" if rank <= depth else f"Counterexample: GQR({rank}) > Depth({depth})"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")