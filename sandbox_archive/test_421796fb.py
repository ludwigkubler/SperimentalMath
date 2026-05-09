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
    
    def schur_functor(n, lambda_):
        if len(lambda_) != 2 or lambda_[0] != n - 1 or lambda_[1] != 1:
            return 0
        partition = (n-1, 1)
        sign = (-1) ** sum(partition[i] * (partition[i] + 1) // 2 for i in range(len(partition)))
        product = math.factorial(n)
        hook_length_formula_value = hook_length_formula(partition, n)
        return sign * product // hook_length_formula_value
    
    def hook_length_formula(shape, n):
        result = 1
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                hook_length = (n - row) + (n - col - shape[row][col]) - 1
                result *= hook_length
        return result
    
    def plethysm_multiplicity(n, lambda_):
        multiplicity = 0
        for partition in partitions(n):
            multiplicity += schur_functor(n, partition)
        return multiplicity
    
    def partitions(n):
        if n == 0:
            yield ()
            return
        for p in partitions(n - 1):
            yield (p + (1,),)
            if len(p) > 0 and p[-1] > 1:
                yield tuple(x - 1 if x == p[-1] else x for x in p) + (1,)
    
    n = random.randint(2, 40)
    plethysm_multiplicity = plethysm_multiplicity(n, (n-1, 1))
    
    return {
        "metric_name": "plethysm_multiplicity",
        "metric_value": plethysm_multiplicity,
        "instances_tested": 1,
        "conjecture_holds": plethysm_multiplicity >= 2**n,
        "counterexample": "" if plethysm_multiplicity >= 2**n else f"plethysm_multiplicity < {2**n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"plethysm_multiplicity < {2**n}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE conjecture_mapping_undefined")