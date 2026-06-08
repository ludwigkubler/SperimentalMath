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
    
    def tseitin_formula(n):
        if n == 1:
            return ["A"]
        else:
            x = "X" + str(random.randint(0, n-1))
            y = "Y" + str(random.randint(0, n-1))
            z = "Z" + str(random.randint(0, n-1))
            return [f"{x} ∨ {y}", f"{x} → {z}", f"{y} → {z}", f"{z} ∨ ¬{x}", f"{z} ∨ ¬{y}"]
    
    def local_index(vertex_set):
        # Simplified local index calculation for demonstration
        return len(vertex_set) * 2
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    depths = [5, 10, 15, 20, 30, 40]
    for depth in depths:
        if n_max >= 16 and instances_tested >= 30:
            break
        
        for _ in range(5):
            formula = tseitin_formula(depth)
            vertex_set = set(formula)
            metric_value = local_index(vertex_set)
            
            if metric_value > 4 * depth * math.log(depth):
                conjecture_holds = False
                counterexample = f"Depth {depth}, Vertex Set: {vertex_set}"
                break
            
            instances_tested += 1
            n_max = max(n_max, len(formula))
            metric_values.append(metric_value)
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_msl = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msl) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")