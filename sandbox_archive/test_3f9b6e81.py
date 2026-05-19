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
    
    # Define the tautology family (e.g., pigeonhole principle)
    def pigeonhole(n):
        return [i for i in range(1, n+1)] * 2
    
    # Simulate proof system P's handling of tautologies
    def prove_tautology(tautology, max_depth):
        if len(tautology) > max_depth:
            return False
        return True
    
    # Define the bounded arithmetic theory S12 (simplified for testing)
    def is_optimal_proof(proof):
        return len(proof) == 1
    
    n = random.randint(5, 40)
    tautology = pigeonhole(n)
    
    max_depth_S12 = n // 2
    max_depth_P = n
    
    proof_S12 = prove_tautology(tautology, max_depth_S12)
    proof_P = prove_tautology(tautology, max_depth_P)
    
    optimal_proof_S12 = is_optimal_proof(proof_S12)
    optimal_proof_P = is_optimal_proof(proof_P)
    
    metric_value = 0
    if optimal_proof_S12 and not optimal_proof_P:
        metric_value = 1
    
    conjecture_holds = (metric_value == 1)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "optimal_proof_exists",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")