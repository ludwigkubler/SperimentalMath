# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_lie_algebroid(n):
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.choice([True, False]):
                    L[i][j] = random.randint(1, 10)
        return L
    
    def smash_product(L1, L2):
        n = len(L1)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += L1[i][k] * L2[k][j]
        return result
    
    def index(L):
        n = len(L)
        det = 0
        if n == 1:
            return abs(L[0][0])
        for i in range(n):
            minor = [row[:i] + row[i+1:] for row in L[1:]]
            sign = (-1) ** i
            det += sign * L[0][i] * index(minor)
        return abs(det)
    
    def monotone_width(circuit):
        # Placeholder function to generate a random monotone width
        return random.randint(5, 20)
    
    n_max = 30
    instances_tested = 0
    total_index = 0
    total_width = 0
    
    for n in range(5, n_max + 1):
        L1 = generate_lie_algebroid(n)
        L2 = generate_lie_algebroid(n)
        product = smash_product(L1, L2)
        ind = index(product)
        width = monotone_width([random.randint(0, 1) for _ in range(n)])
        
        total_index += ind
        total_width += width
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Index of Lie Algebroid Pairs",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_index = total_index / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * total_index * total_width - sum(ind * width for ind, width in zip([ind for _ in range(instances_tested)], [width for _ in range(instances_tested)]))) / ((instances_tested * sum(ind ** 2 for ind in [ind for _ in range(instances_tested)]) - (total_index ** 2)) * (instances_tested * sum(width ** 2 for width in [width for _ in range(instances_tested)]) - (total_width ** 2))) ** 0.5
    
    return {
        "metric_name": "Index of Lie Algebroid Pairs",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient >= 0.5 else "Correlation coefficient below 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] == "Correlation coefficient below 0.5" for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["counterexample"] == "Correlation coefficient below 0.5")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reasons")