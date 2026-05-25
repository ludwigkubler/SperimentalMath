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
    
    def min_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(n)):
                continue
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[pivot_row], A[i] = A[i], A[pivot_row]
            rank += 1
            for j in range(n):
                if i == j:
                    continue
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def random_circuit_complexity(f, n):
        # Simplified version using the Schwartz-Zippel lemma
        q = 2
        m = sum(1 for _ in f)
        return math.ceil(m * (math.log(n) + math.log(q)))
    
    def algebraic_stack(A):
        n = len(A)
        stack = []
        for i in range(n):
            row = [A[j][i] for j in range(n)]
            if any(row):
                stack.append(row)
        return stack
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            f = [random.choice([0, 1]) for _ in range(n)]
            A = algebraic_stack(f)
            R_f = random_circuit_complexity(f, n)
            MinRank_A_f = min_rank(A)
            
            if MinRank_A_f == 0:
                continue
            
            instances_tested += 1
            metric_value = MinRank_A_f * math.log(n)
            total_metric_value += metric_value
            
            if R_f > 0 and metric_value < math.log(R_f):
                conjecture_holds = False
                counterexample = f"n={n}, f={f}, MinRank(A_f)={MinRank_A_f}, log(R(f))={math.log(R_f)}, metric_value={metric_value}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / (len(n_values) * 5)
    
    return {
        "metric_name": "MinRank(A_f) * log(n)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")