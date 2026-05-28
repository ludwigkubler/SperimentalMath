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
    
    def hypergeometric_function_rank(f):
        n = int(math.log2(len(f)))
        if n == 0: return 0
        rank = 1
        while True:
            found_non_zero = False
            for i in range(n + 1):
                coeff = sum([f[j] * (-1)**(j & (i - 1)) for j in range(len(f)) if bin(j).count('1') == i]) / math.comb(len(f), i)
                if coeff != 0:
                    found_non_zero = True
            if not found_non_zero:
                return rank - 1
            rank += 1
    
    def communication_complexity(n):
        return n
    
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(3, 40))
        r_f = hypergeometric_function_rank(f)
        CC_XOR_n = communication_complexity(len(f))
        if CC_XOR_n < r_f * math.log2(len(f)):
            return {
                "metric_name": "communication_complexity",
                "metric_value": CC_XOR_n,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"CC_XOR({len(f)}) < r_f * log2(n)"
            }
        metric_values.append(CC_XOR_n)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for v in metric_values if v >= r_f * math.log2(len(f))) / instances_tested
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='CC_XOR(n) < r_f * log2(n)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")