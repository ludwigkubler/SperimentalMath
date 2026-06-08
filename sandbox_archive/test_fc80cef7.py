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
    
    def generate_quandle(n):
        quandle = []
        for i in range(n):
            row = [0] * n
            for j in range(i, n):
                row[j] = random.randint(1, 2)
            quandle.append(row)
        return quandle
    
    def max_clauses_satisfiable(quandle):
        n = len(quandle)
        max_sat = 0
        for i in range(1 << n):
            satisfied = True
            for j in range(n):
                if (i >> j) & 1:
                    for k in range(j, n):
                        if quandle[j][k] == 2 and ((i >> k) & 1) != 0:
                            satisfied = False
                            break
                    if not satisfied:
                        break
            if satisfied:
                max_sat += 1
        return max_sat
    
    def minimal_local_cohesion_index(quandle):
        n = len(quandle)
        mci = float('inf')
        for i in range(n):
            for j in range(i, n):
                if quandle[i][j] == 2:
                    count = 0
                    for k in range(j, n):
                        if quandle[j][k] == 2 and (quandle[i][k] == 1 or quandle[k][i] == 1):
                            count += 1
                    mci = min(mci, count)
        return mci
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        quandle = generate_quandle(n)
        max_sat = max_clauses_satisfiable(quandle)
        mci = minimal_local_cohesion_index(quandle)
        
        if mci > 2 ** max_sat:
            return {
                "metric_name": "minimal_local_cohesion_index",
                "metric_value": mci,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"mci({n}) = {mci} > 2^{max_sat}"
            }
        
        metric_values.append(mci)
    
    mean_msl = sum(metric_values) / len(metric_values)
    std_msl = math.sqrt(sum((x - mean_msl) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "minimal_local_cohesion_index",
        "metric_value": mean_msl,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_msl = sum(result["metric_value"] for result in results) / len(results)
    std_msl = math.sqrt(sum((result["metric_value"] - mean_msl) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_msl} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")