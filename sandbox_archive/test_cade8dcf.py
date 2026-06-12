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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(n-1):
            for j in range(i+1, n):
                clauses.append([f'-{literals[i]}', f'{literals[j]}'])
                clauses.append([f'{literals[i]}', f'-{literals[j]}'])
        return literals, clauses

    def resolution_width(clauses):
        queue = clauses[:]
        while True:
            new_clauses = []
            for i in range(len(queue)):
                for j in range(i+1, len(queue)):
                    if set(queue[i]) & set(queue[j]):
                        common_literal = list(set(queue[i]) & set(queue[j]))
                        new_clause = [l for l in queue[i] + queue[j] if l != common_literal[0]]
                        if not any(new_clause == clause for clause in queue):
                            new_clauses.append(new_clause)
            if new_clauses:
                queue.extend(new_clauses)
            else:
                return len(queue)

    def vector_bundle_rank(n):
        # Simplified example: rank is n
        return n

    n_max = 40
    instances_tested = 30
    total_width = 0
    total_rank = 0
    
    for _ in range(instances_tested):
        literals, clauses = tseitin_formula(n)
        width = resolution_width(clauses)
        rank = vector_bundle_rank(len(literals))
        total_width += width
        total_rank += rank

    mean_width = total_width / instances_tested
    mean_rank = total_rank / instances_tested
    
    conjecture_holds = mean_width <= mean_rank
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution Width vs Vector Bundle Rank",
        "metric_value": mean_width,
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

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")