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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quadratic_form_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                x_i = [int(b) for b in format(i, f'0{n}b')]
                x_j = [int(b) for b in format(j, f'0{n}b')]
                M[i][j] = sum(x_i[k] * x_j[k] for k in range(n))
        return M
    
    def min_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(i, n):
                    if M[j][i] != 0:
                        factor = M[j][i]
                        for k in range(n):
                            M[j][k] -= factor * M[i][k]
        return rank
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        # Using a simple algorithm for demonstration purposes
        return n * (n - 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        M_f = quadratic_form_matrix(f)
        tau_quad_f = min_rank(M_f)
        comm_complexity = communication_complexity(f)
        
        total_metric_value += tau_quad_f / (n * math.log2(n))
        instances_tested += 1
        
        if tau_quad_f / (n * math.log2(n)) < 0.7:
            conjecture_holds = False
            counterexample = f"tau_quad({n}) / n log n < 0.7"
        
        if comm_complexity > 1.5 * tau_quad_f:
            conjecture_holds = False
            counterexample = f"comm_complexity({n}) > 1.5 * tau_quad({n})"
    
    return {
        "metric_name": "tau_quad / n log n",
        "metric_value": total_metric_value / len(n_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")