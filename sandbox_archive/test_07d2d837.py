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
    
    def generate_ac0_circuit(n):
        if n == 1:
            return [False]
        else:
            left = generate_ac0_circuit(n // 2)
            right = generate_ac0_circuit(n - n // 2)
            return [left[i] and right[i] for i in range(len(left))]
    
    def tropicalized_heegaard_rank(circuit):
        size = len(circuit)
        rank = 0
        for i in range(size):
            if circuit[i]:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        rank = tropicalized_heegaard_rank(circuit)
        size = len(circuit)
        if size == 0:
            continue
        c = 1 / math.log(size)
        if rank < c * math.log(size):
            results.append({"n": n, "rank": rank, "size": size, "c": c, "conjecture_holds": False})
        else:
            results.append({"n": n, "rank": rank, "size": size, "c": c, "conjecture_holds": True})
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_values = [r["rank"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds_fraction >= 0.8,
        "counterexample": "" if all(r["conjecture_holds"] for r in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    conjecture_holds_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={conjecture_holds_fraction}")
    elif conjecture_holds_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={conjecture_holds_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")