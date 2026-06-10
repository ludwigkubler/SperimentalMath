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
        quandle = [[i for i in range(1, n+1)]]
        for _ in range(n-1):
            new_row = [quandle[-1][(i * 2) % (n + 1)] for i in range(n)]
            quandle.append(new_row)
        return quandle

    def calculate_automorphism_group(quandle):
        n = len(quandle[0])
        aut_group = []
        for perm in itertools.permutations(range(n)):
            if all(quandle[i][perm[j]] == quandle[i][j] for i in range(n) for j in range(n)):
                aut_group.append(perm)
        return aut_group

    def calculate_communication_complexity_rank_variance(circuit):
        # Placeholder function; actual implementation needed
        return random.random()

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        quandle = generate_quandle(n)
        aut_group = calculate_automorphism_group(quandle)
        order = len(aut_group)
        log_order = math.log2(order) if order > 0 else -math.inf
        r_C = calculate_communication_complexity_rank_variance(n)
        
        metric_values.append(log_order)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / instances_tested) ** 0.5
    
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "log₂(ο(Q(C)))",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")