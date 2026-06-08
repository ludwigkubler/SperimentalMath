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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c != 0 for c in clause):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            if not any(abs(lit) in seen for lit in clause):
                seen.update(abs(lit) for lit in clause)
                new_clauses = []
                for other_clause in queue:
                    if any(-lit in other_clause for lit in clause):
                        for lit in set(other_clause) - {0}:
                            new_clause = [l for l in other_clause if l != -lit]
                            if new_clause and all(abs(lit) not in seen for lit in new_clause):
                                new_clauses.append(new_clause)
                queue.extend(new_clauses)
        return len(queue)
    
    def hopf_algebra_rank(cnf):
        # Simplified rank calculation based on clause count
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    rank = hopf_algebra_rank(cnf)
    
    if width == 0:
        return {
            "metric_name": "min_rank_to_width_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    ratio = rank / width
    return {
        "metric_name": "min_rank_to_width_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        ratios = [r["metric_value"] for r in results]
        mean_ratio = sum(ratios) / len(ratios)
        std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
        support_fraction = sum(0.5 <= r["metric_value"] <= 2 for r in results) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not (0.5 <= r["metric_value"] <= 2))
            print(f"RESULT: FALSIFIED counterexample=\"out_of_range\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE some_ratios_are_none")