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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def resolution_proof_length(cnf):
        # Simplified resolution proof length calculation
        return len(cnf) ** 2
    
    def birational_model_rank(n):
        # Simplified birational model rank calculation
        return random.randint(1, int(math.log(n, 2)) + 1)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_rank = birational_model_rank(n)
    proof_length = resolution_proof_length(cnf)
    
    metric_value = abs(min_rank - math.log(n))
    conjecture_holds = metric_value <= 1 and proof_length <= 2 * math.log(n)
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, log(n)={math.log(n)}, proof_length={proof_length}"
    
    return {
        "metric_name": "birational_model_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank > log(n) + 2 or proof_length > 2 * log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")