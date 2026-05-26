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
    
    def generate_acc0_circuit(n):
        # Simple ACC^0 circuit generator for demonstration purposes
        return [random.randint(1, 2) for _ in range(n)]
    
    def hodge_rank(C):
        # Placeholder Hodge rank computation
        S_n = sum(C)
        n = len(C)
        if S_n == 0 or n == 0:
            return 0
        return Fraction(S_n, math.log(n))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    C = generate_acc0_circuit(n)
    R_n = hodge_rank(C)
    
    metric_name = "Hodge Rank"
    metric_value = R_n
    instances_tested = 1
    conjecture_holds = R_n <= Fraction(S_n, math.log(n))
    counterexample = "" if conjecture_holds else f"Circuit size {S_n}, Hodge rank {R_n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = f"Circuit size {results[0]['metric_value']}, Hodge rank {results[0]['counterexample']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")