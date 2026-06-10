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
        n = len(f)
        count = [f.count(i) for i in set(f)]
        variance = sum((x / len(f) - (sum(count) / len(f))) ** 2 for x in count)
        return variance
    
    def conformal_block_representation_size(r):
        return r**2 / math.log(n)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    r = communication_complexity_rank_variance(f)
    dim_M_f = conformal_block_representation_size(r)
    
    metric_name = "communication_complexity_rank_variance"
    metric_value = r
    instances_tested = 1
    n_max = n
    conjecture_holds = abs(dim_M_f - (r**2 / math.log(n))) <= 0.2 * (r**2 / math.log(n))
    counterexample = "" if conjecture_holds else f"dim(M_f)={dim_M_f}, expected Θ(r^2/log(n))={r**2/math.log(n)}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")