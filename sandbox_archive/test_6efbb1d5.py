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
        cnf = []
        for _ in range(random.randint(1, n * (n - 1))):
            clause = [random.choice([i, -i]) for i in range(1, n + 1)]
            random.shuffle(clause)
            cnf.append(tuple(clause))
        return cnf
    
    def frege_proof_depth(cnf):
        # Simplified estimation of Frege proof depth
        return len(cnf) * (len(cnf[0]) + 1)
    
    def hodge_arakelov_index(n):
        # Simplified estimation of Hodge-Arakelov index
        return n ** 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_ai = 0
        total_depth = 0
        
        for _ in range(5):
            cnf = generate_cnf(n)
            ai = hodge_arakelov_index(n)
            depth = frege_proof_depth(cnf)
            
            if ai > 10 or depth > 10:
                return {
                    "metric_name": "Pearson correlation",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "AI(K(φ)) or d(φ) exceeds 10"
                }
            
            total_ai += ai
            total_depth += depth
            instances_tested += 1
        
        avg_ai = total_ai / instances_tested
        avg_depth = total_depth / instances_tested
        results.append((avg_ai, avg_depth))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "AI(K(φ)) or d(φ) exceeds 10"
        }
    
    ai_values = [r[0] for r in results]
    depth_values = [r[1] for r in results]
    
    n_max = max([max(r) for r in results])
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_dev_x * std_dev_y)
    
    correlation = pearson_correlation(ai_values, depth_values)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")