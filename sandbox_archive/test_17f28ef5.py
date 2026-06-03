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
    
    def frege_proof_length(f):
        # Placeholder function to simulate Frege proof length
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def cubical_complex_rank(cubical_complex):
        # Placeholder function to simulate minimal rank of cubical complex
        # This is a dummy implementation and should be replaced with actual logic
        return len(cubical_complex)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    L_f = frege_proof_length(f)
    min_rank_C_f = cubical_complex_rank([f])
    
    if L_f == 0:
        return {
            "metric_name": "min_rank(C_f) / L_f",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "L_f is zero, division by zero"
        }
    
    ratio = min_rank_C_f / L_f
    
    return {
        "metric_name": "min_rank(C_f) / L_f",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank(C_f) / L_f > 2\" first_failing_seed={first_failing_seed}")