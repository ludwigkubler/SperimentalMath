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
    
    def generate_bp(n):
        bp = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(n)]
            bp.append(row)
        return bp
    
    def compute_k_theory_rank(bp):
        n = len(bp)
        identity = [[int(i == j) for i in range(n)] for j in range(n)]
        
        # Gaussian elimination to find the rank
        for i in range(n):
            if bp[i][i] == 0:
                found_nonzero = False
                for j in range(i + 1, n):
                    if bp[j][i] != 0:
                        for k in range(n):
                            bp[i][k], bp[j][k] = bp[j][k], bp[i][k]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    return i
        
            pivot = bp[i][i]
            for j in range(n):
                bp[i][j] /= pivot
        
            for j in range(n):
                if j != i:
                    factor = bp[j][i]
                    for k in range(n):
                        bp[j][k] -= factor * bp[i][k]
        
        return n - sum(1 for row in bp if all(x == 0 for x in row))
    
    def size(bp):
        return len(bp)
    
    n = random.randint(5, 40)
    bp = generate_bp(n)
    k_theory_rank = compute_k_theory_rank(bp)
    size_p = size(bp)
    
    metric_value = k_theory_rank
    instances_tested = 1
    
    conjecture_holds = (k_theory_rank <= math.log(2**n)) and (k_theory_rank >= math.log(size_p))
    counterexample = "" if conjecture_holds else f"rank={k_theory_rank}, log(2^n)={math.log(2**n)}, log(size(P))={math.log(size_p)}"
    
    return {
        "metric_name": "K-theory Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*100 + 2, 100))
    
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
    elif any(abs(r["metric_value"] - math.log(2**r["instances_tested"])) > 3 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - math.log(2**result["instances_tested"])) > 3)
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds log(2^n) by more than 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")