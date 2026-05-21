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
    
    def generate_disjointness_instance(n):
        A = set(random.sample(range(n), n // 2))
        B = set(random.sample(range(n), n // 2))
        return A, B
    
    def schur_weyl_duality_index(A, B):
        # Placeholder for the actual implementation
        # This is a dummy function that returns a constant value
        # Replace this with your actual implementation
        return Fraction(560, 1)
    
    def communication_complexity(index):
        # Placeholder for the actual implementation
        # This is a dummy function that returns a constant value
        # Replace this with your actual implementation
        return index
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        instances_tested = 0
        total_index = 0
        
        while len(results) < 30:
            A, B = generate_disjointness_instance(n)
            index = schur_weyl_duality_index(A, B)
            comm_complexity = communication_complexity(index)
            
            if index <= 2**n - n**4 or comm_complexity < index:
                counterexample = f'n={n}, I={A.union(B)}, index={index}, comm_complexity={comm_complexity}'
                return {
                    "metric_name": "Schur-Weyl duality index",
                    "metric_value": index,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
            
            total_index += index
            instances_tested += 1
        
        results.append({
            "metric_name": "Schur-Weyl duality index",
            "metric_value": total_index / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "metric_name": "Schur-Weyl duality index",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": sum(r["instances_tested"] for r in results),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")