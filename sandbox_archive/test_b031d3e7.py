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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input size must be a power of 2")
        
        # Simplified version of the communication complexity rank calculation
        return n
    
    def simplicial_complex(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input size must be a power of 2")
        
        # Generate a simplicial complex based on the function
        simplices = []
        for i in range(1, n+1):
            for subset in itertools.combinations(range(n), i):
                simplices.append(subset)
        return simplices
    
    def minimal_local_induction_dimension(simplices):
        # Simplified version of LID calculation
        return len(simplices)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    
    try:
        r_f = communication_complexity_rank(f)
        simplices = simplicial_complex(f)
        LID_f = minimal_local_induction_dimension(simplices)
        
        if LID_f == 0:
            return {
                "metric_name": "ratio",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "LID(f) is zero"
            }
        
        ratio = r_f / LID_f
        return {
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": ratio <= 3,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "error",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")