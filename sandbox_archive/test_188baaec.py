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
    
    def quadratic_form_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << n):
                sum_product = 0
                for k in range(n):
                    x_i = (i >> k) & 1
                    x_j = (j >> k) & 1
                    sum_product += f[(x_i, x_j)]
                M[i][j] = sum_product
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        # Using a simple deterministic algorithm for demonstration
        return 2 ** (n - 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        M_f = quadratic_form_matrix(f)
        tau_quad_f = min_rank(M_f)
        comm_complexity = communication_complexity(f)
        
        if tau_quad_f == 0 or comm_complexity > 1.5 * tau_quad_f:
            return {
                "metric_name": "tau_quad / n log n",
                "metric_value": -1,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, tau_quad={tau_quad_f}, comm_complexity={comm_complexity}"
            }
        
        total_metric_value += tau_quad_f / (n * math.log(n))
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "tau_quad / n log n",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_metric_value >= 0.9 and comm_complexity <= 1.2 * tau_quad_f,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["instances_tested"] == 0 for r in results):
        print("RESULT: INCONCLUSIVE no_trials_run")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")