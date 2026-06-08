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
        quandle = []
        for i in range(n):
            row = [random.randint(0, n-1) for _ in range(n)]
            quandle.append(row)
        return quandle
    
    def apply_quandle(quandle, x):
        n = len(quandle)
        result = []
        for i in range(n):
            result.append(quandle[x][i])
        return result
    
    def max_clauses_satisfiable(clauses):
        n = len(clauses[0])
        if not clauses:
            return 0
        max_sat = 0
        for mask in range(1 << n):
            satisfied = True
            for clause in clauses:
                if all((mask >> j) & 1 == (x < 0 and -x or x) % n in clause for x in clause):
                    continue
                else:
                    satisfied = False
                    break
            if satisfied:
                max_sat += 1
        return max_sat
    
    def minimal_local_cohesion_index(quandle):
        n = len(quandle)
        index = 0
        for i in range(n):
            for j in range(i+1, n):
                if quandle[i][j] == quandle[j][i]:
                    index += 1
        return index
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = random.sample(range(1, n+1), random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            quandle = generate_quandle(n)
            clauses = generate_sat_instance(n)
            mci = minimal_local_cohesion_index(quandle)
            max_sat = max_clauses_satisfiable(clauses)
            metric_values.append(mci <= 2**max_sat)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    support_fraction = sum(metric_values) / len(metric_values)
    
    if all(metric_values):
        return {
            "metric_name": "mci <= 2^(max_clauses_satisfiable)",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for i, mci in enumerate(metric_values):
            if not mci:
                counterexample = f"mci({i}) > 2^(max_clauses_satisfiable)"
                break
        return {
            "metric_name": "mci <= 2^(max_clauses_satisfiable)",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")