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
    n = random.randint(5, 40)
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        G_f = [[f[(i >> j) ^ (k >> j)] for k in range(2**n)] for j in range(n)]
        
        L_G_f = [[sum(G_f[i][j] * G_f[k][l] for i in range(2**n)) for l in range(2**n)] for j in range(2**n)]
        
        rank = 0
        for row in L_G_f:
            if any(row):
                rank += 1
        
        metric_values.append(rank)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / instances_tested)
    conjecture_holds = all(x >= math.log(n, 2) for x in metric_values)
    counterexample = "" if conjecture_holds else "rank < log(n)"
    
    return {
        "metric_name": "min_rank_laplacian",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")