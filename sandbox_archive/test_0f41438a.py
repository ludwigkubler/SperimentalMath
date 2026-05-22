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
    
    def generate_quandle(n, r):
        quandle = []
        for i in range(r):
            row = [0] * n
            for j in range(i + 1, n):
                row[j] = random.randint(0, n - 1)
            quandle.append(row)
        return quandle
    
    def communication_complexity(quandle, n):
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if quandle[i][j] == quandle[j][i]:
                    complexity += 1
        return complexity
    
    n = random.randint(5, 40)
    r = random.randint(1, min(3, n - 1))
    quandle = generate_quandle(n, r)
    cc = communication_complexity(quandle, n)
    
    metric_value = cc / (n ** r)
    return {
        "metric_name": "Communication Complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if metric_value >= 1 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 1 / (2 * min(3, n - 1)) for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='communication_complexity_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")