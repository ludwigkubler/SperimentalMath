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
    
    def min_rank(A_f):
        # Placeholder implementation of min rank calculation
        return len(A_f)
    
    def randomized_circuit_complexity(f, n):
        if n == 1:
            return 1
        k = random.randint(1, n-1)
        m = 2**n
        B = [[random.choice([0, 1]) for _ in range(k)] for _ in range(m)]
        D = [f(x) ^ sum(B[i][j] * x[j] for j in range(k)) for i in range(m)]
        return k + randomized_circuit_complexity(D, n-1)
    
    def algebraic_stack(f):
        # Placeholder implementation of algebraic stack calculation
        return [[i for i in range(len(f)) if f[i] == 1]]
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    A_f = algebraic_stack(f)
    R_f = randomized_circuit_complexity(f, n)
    MinRank_A_f = min_rank(A_f)
    
    metric_value = MinRank_A_f * math.log(n)
    conjecture_holds = False
    counterexample = ""
    
    if R_f > 0:
        ratio = MinRank_A_f / math.log(n)
        if ratio < 1e-6:
            conjecture_holds = True
    
    return {
        "metric_name": "MinRank(A_f) * log(n)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = f"MinRank(A_f) * log(n) = {res['metric_value']}, R(f) = {randomized_circuit_complexity(generate_boolean_function(5), 5)}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(res)]}")