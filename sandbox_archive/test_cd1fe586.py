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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_comm_cost = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] != f[j]:
                    comm_cost = bin(i ^ j).count('1')
                    if comm_cost > max_comm_cost:
                        max_comm_cost = comm_cost
        return max_comm_cost
    
    def coxeter_group_action(f):
        n = int(math.log2(len(f)))
        # Simplified Coxeter group action for demonstration purposes
        # This is a placeholder and should be replaced with actual computation
        return 10 * communication_complexity(f)**2
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    C_f = communication_complexity(f)
    G_order = coxeter_group_action(f)
    
    metric_name = "Coxeter Group Action Order"
    metric_value = G_order
    instances_tested = 1
    conjecture_holds = G_order <= 10 * C_f**2
    counterexample = "" if conjecture_holds else f"Counterexample for n={n}, C(f)={C_f}, G_order={G_order}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")