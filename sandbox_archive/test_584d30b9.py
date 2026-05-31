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
    
    def generate_boolean_function(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        m = len(f[0])
        max_comm = 0
        for i in range(2**n):
            comm = sum(f[i][j] for j in range(m) if f[i][j] != f[(i ^ (1 << random.randint(0, n-1))) % (2**n)][j])
            max_comm = max(max_comm, comm)
        return max_comm
    
    def minimal_local_zeta_function_size(f):
        n = len(f)
        m = len(f[0])
        zeta_sum = 0
        for i in range(2**n):
            for j in range(m):
                if f[i][j] == 1:
                    zeta_sum += math.log2(i + 1)
        return zeta_sum
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    mzeta_values = []
    c_values = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n, random.randint(1, n))
            c = communication_complexity(f)
            mzeta = minimal_local_zeta_function_size(f)
            mzeta_values.append(mzeta)
            c_values.append(c)
            instances_tested += 1
    
    if not mzeta_values or not c_values:
        return {
            "metric_name": "mzeta vs c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((mzeta - mean_mzeta) * (c - mean_c) for mzeta, c in zip(mzeta_values, c_values)) / math.sqrt(sum((mzeta - mean_mzeta)**2 for mzeta in mzeta_values) * sum((c - mean_c)**2 for c in c_values))
    mean_mzeta = sum(mzeta_values) / len(mzeta_values)
    mean_c = sum(c_values) / len(c_values)
    
    if correlation_coefficient < 0.7:
        return {
            "metric_name": "mzeta vs c",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Correlation coefficient {correlation_coefficient} < 0.7"
        }
    
    if any(abs(mzeta - c) > 2 for mzeta, c in zip(mzeta_values, c_values)):
        return {
            "metric_name": "mzeta vs c",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Max deviation {max(abs(mzeta - c) for mzeta, c in zip(mzeta_values, c_values))} > 2"
        }
    
    return {
        "metric_name": "mzeta vs c",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.7 or max deviation > 2\" first_failing_seed={first_failing_seed}")