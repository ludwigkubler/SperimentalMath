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
    
    def dpll(instance):
        # Simplified DPLL algorithm for demonstration purposes
        if not instance:
            return 1
        literal = next(iter(instance))
        pos_clauses = [c for c in instance if literal in c]
        neg_clauses = [c for c in instance if literal in [-l for l in c]]
        if not pos_clauses and not neg_clauses:
            return 0
        if any(not dpll(c) for c in pos_clauses):
            return dpll([c for c in instance if literal not in c])
        return dpll([c for c in instance if -literal not in c])

    def hodge_arc_length(instance):
        # Simplified Hodge arc length calculation
        n = len(instance)
        return Fraction(n, 2)

    instances_tested = 0
    n_max = 0
    total_correlation = 0
    count_supports_conjecture = 0

    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested += n
        n_max = max(n_max, n)
        
        for _ in range(5):
            instance = [[random.randint(-n, n) for _ in range(random.randint(1, n))] for _ in range(random.randint(1, n))]
            dpll_width = dpll(instance)
            arc_length = hodge_arc_length(instance)
            
            if dpll_width == 0 or arc_length == 0:
                continue
            
            correlation = (dpll_width - arc_length) / (dpll_width + arc_length)
            total_correlation += correlation
    
    mean_correlation = Fraction(total_correlation, instances_tested)
    
    conjecture_holds = mean_correlation > Fraction(8, 10)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hodge Arc Length vs DPLL Width Correlation",
        "metric_value": float(mean_correlation),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")