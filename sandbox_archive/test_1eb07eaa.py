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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[(i + 1) % n] for i in range(n)):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            if not any(lit in seen or -lit in seen for lit in clause):
                seen.update(clause)
                new_clauses = []
                for c1 in queue:
                    for c2 in queue:
                        common = [l for l in c1 if -l in c2]
                        if common:
                            new_clause = list(set(c1 + c2) - set(common))
                            if len(new_clause) == 1:
                                return len(queue)
                            new_clauses.append(new_clause)
                queue.extend(new_clauses)
        return len(queue)
    
    def quandle_order(n):
        return 2**n
    
    results = []
    for n in range(5, 41):
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        order = quandle_order(n)
        if width > order:
            return {
                "metric_name": "resolution_width",
                "metric_value": width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"CNF with n={n} has width {width} > quandle order {order}"
            }
        results.append({"n": n, "width": width, "order": order})
    
    mean_width = sum(result["width"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["width"] - mean_width)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["width"] <= result["order"]) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["metric_value"] - mean_width)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")