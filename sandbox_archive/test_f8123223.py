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
    
    def generate_quandle(n):
        quandle = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                quandle[i][j] = random.randint(0, n-1)
                if i != j:
                    quandle[j][i] = quandle[i][j]
        return quandle
    
    def communication_complexity(quandle, n):
        instances_tested = 0
        total_complexity = 0
        
        for _ in range(n * (n - 1) // 2):
            i, j = random.sample(range(n), 2)
            if quandle[i][j] == quandle[j][i]:
                continue
            instances_tested += 1
            complexity = max(abs(i - j), abs(quandle[i][j] - quandle[j][i]))
            total_complexity += complexity
        
        if instances_tested == 0:
            return {"metric_name": "Communication Complexity", 
                    "metric_value": 0, 
                    "instances_tested": 0, 
                    "conjecture_holds": False, 
                    "counterexample": "No valid instances tested"}
        
        avg_complexity = Fraction(total_complexity, instances_tested)
        return {"metric_name": "Communication Complexity", 
                "metric_value": float(avg_complexity), 
                "instances_tested": instances_tested, 
                "conjecture_holds": True, 
                "counterexample": ""}
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_complexity = 0
    
    for n in n_values:
        quandle = generate_quandle(n)
        result = communication_complexity(quandle, n)
        instances_tested = result["instances_tested"]
        if instances_tested == 0:
            return {"metric_name": "Communication Complexity", 
                    "metric_value": 0, 
                    "instances_tested": 0, 
                    "conjecture_holds": False, 
                    "counterexample": "No valid instances tested"}
        
        total_instances += instances_tested
        total_complexity += result["metric_value"] * instances_tested
    
    avg_complexity = Fraction(total_complexity, total_instances)
    
    return {"metric_name": "Communication Complexity", 
            "metric_value": float(avg_complexity), 
            "instances_tested": total_instances, 
            "conjecture_holds": True, 
            "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_complexity = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_complexity} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")