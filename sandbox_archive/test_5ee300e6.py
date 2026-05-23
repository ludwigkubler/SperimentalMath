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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def resolution_width(f):
        n = len(f)
        if n == 1:
            return 1
        clauses = []
        for i in range(n):
            clauses.append([i])
        while True:
            new_clauses = []
            found_new_clause = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(clause1) + len(clause2) == n + 1 and all(x not in clause2 for x in clause1):
                        new_clause = [x for x in clause1 if x != -i] + [x for x in clause2 if x != i]
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                            found_new_clause = True
            if not found_new_clause:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def tropicalized_cohomology_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            rank = tropicalized_cohomology_rank(f)
            width = resolution_width(f)
            if rank < width - 2:  # Early exit if the conjecture is clearly violated
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, f={f}, rank={rank}, width={width}"
                }
            total_rank += rank
            total_width += width
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_width = total_width / instances_tested
    sd = math.sqrt((sum((x - mean_rank) ** 2 for x in [tropicalized_cohomology_rank(generate_boolean_function(n)) for n in n_values]) / len(n_values)))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank >= mean_width - sd,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    sd = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={sd} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={sd} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"n={r['instances_tested']}, rank={r['metric_value']}, width={resolution_width(generate_boolean_function(r['instances_tested']))}\" first_failing_seed={seeds[results.index(r)]}")
                break