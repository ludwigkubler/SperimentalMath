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
    
    def ac0_circuits(n, d):
        # Placeholder for generating AC⁰ circuits computing PARITY on n inputs with depth d
        return []  # Replace with actual circuit generation logic
    
    def tropical_variety(circuit):
        # Placeholder for computing the tropical variety of a given circuit
        return None  # Replace with actual tropical variety computation logic
    
    def hodge_structure(tropical_variety):
        # Placeholder for determining the Hodge structure over a tropical variety
        return None  # Replace with actual Hodge structure computation logic
    
    def minimal_rank(hodge_structure):
        # Placeholder for computing the minimal rank of the Hodge structure
        return None  # Replace with actual minimal rank computation logic
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different circuits
            d = random.randint(1, 10)  # Random depth between 1 and 10
            circuit = ac0_circuits(n, d)
            tv = tropical_variety(circuit)
            hs = hodge_structure(tv)
            rank = minimal_rank(hs)
            
            if rank is not None:
                results.append({
                    "n": n,
                    "d": d,
                    "rank": rank
                })
    
    if len(results) < 30:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["rank"] - mean_rank) <= 3 * std_dev) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_data")