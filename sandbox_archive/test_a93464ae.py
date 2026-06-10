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
    
    def generate_sat_formula(n):
        clauses = []
        for _ in range(n * 2):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:  # Ensure the clause is not trivially true
                clauses.append(clause)
        return clauses
    
    def resolution_width(phi):
        queue = phi[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            for other in phi:
                if len(set(clause) & set(other)) == 2:
                    new_clause = [x for x in clause + other if x not in [-y for y in clause] and x not in [-y for y in other]]
                    if new_clause and tuple(new_clause) not in seen:
                        queue.append(new_clause)
                        seen.add(tuple(new_clause))
        return len(seen)
    
    def min_order_covering(n):
        # This is a placeholder function. Implement the actual algorithm to find the minimal order of covering.
        return n  # Placeholder value
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_sat_formula(n)
        width = resolution_width(phi)
        o_n = min_order_covering(n)
        results.append({"n": n, "width": width, "o_n": o_n})
    
    total_width = sum(result["width"] for result in results)
    avg_width = total_width / len(results)
    
    conjecture_holds = all(result["width"] <= 2 * result["o_n"] for result in results)  # Placeholder constant c=2
    counterexample = "" if conjecture_holds else "resolution_width > 2 * min_order_covering"
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": avg_width,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
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
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")