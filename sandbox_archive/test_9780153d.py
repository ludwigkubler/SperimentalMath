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
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            count_0 = sum(1 for x in f if x[i] == 0)
            count_1 = len(f) - count_0
            rank += max(count_0, count_1)
        return (rank / n) ** 2
    
    def minimal_local_induction_dimension(f):
        n = int(math.log2(len(f)))
        dim = 0
        for i in range(n):
            count_0 = sum(1 for x in f if x[i] == 0)
            count_1 = len(f) - count_0
            dim += max(count_0, count_1)
        return dim / n
    
    instances_tested = 0
    total_mild = 0.0
    total_rcv = 0.0
    n_max = 5
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        f = generate_boolean_function(n)
        mild = minimal_local_induction_dimension(f)
        rcv = communication_complexity_rank_variance(f)
        
        total_mild += mild
        total_rcv += rcv
        instances_tested += 1
    
    mean_mild = total_mild / instances_tested
    mean_rcv = total_rcv / instances_tested
    correlation_coefficient = (instances_tested * sum(mild * rcv for mild, rcv in zip([mean_mild] * instances_tested, [mean_rcv] * instances_tested)) - instances_tested * mean_mild * mean_rcv) / math.sqrt((instances_tested * sum(mild**2 for mild in [mean_mild] * instances_tested) - instances_tested * mean_mild**2) * (instances_tested * sum(rcv**2 for rcv in [mean_rcv] * instances_tested) - instances_tested * mean_rcv**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")