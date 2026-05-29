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
    
    def dpll_size(f):
        n = len(f)
        states = [{'assignment': [0] * n, 'unsatisfied': f[:]}]
        while states:
            state = states.pop()
            if not state['unsatisfied']:
                return 1
            var = next((i for i in range(n) if any(row[i] == 1 for row in state['unsatisfied'])), None)
            if var is None:
                continue
            for val in [0, 1]:
                new_assignment = state['assignment'].copy()
                new_assignment[var] = val
                new_unsatisfied = [row[:] for row in state['unsatisfied']]
                for i in range(n):
                    if new_assignment[i] == (1 - val) and new_unsatisfied[i][var] == 1:
                        new_unsatisfied[i][var] = 0
                        new_unsatisfied[i] = [x for x in new_unsatisfied[i] if x != 0]
                states.append({'assignment': new_assignment, 'unsatisfied': new_unsatisfied})
        return float('inf')
    
    def symplectic_capacity(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = M + I
        B = I + M
        C = []
        for i in range(n):
            row = [A[i][j] ^ B[j][i] for j in range(n)]
            C.append(row)
        det_C = determinant(C)
        return math.log2(det_C) / n
    
    def determinant(M):
        n = len(M)
        if n == 1:
            return M[0][0]
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in M[1:]]
            det += (-1) ** i * M[0][i] * determinant(submatrix)
        return det
    
    def boolean_function(n, seed):
        random.seed(seed)
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = boolean_function(n, seed)
        M_f = [[f[i][j] ^ f[j][i] for j in range(n)] for i in range(n)]
        t_star = dpll_size(f)
        if t_star == float('inf'):
            continue
        cap = symplectic_capacity(M_f)
        results.append({
            'n': n,
            't_star': t_star,
            'cap': cap,
            'diff': abs(cap - math.log2(t_star))
        })
    
    if not results:
        return {
            "metric_name": "symplectic_capacity_diff",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = sum(result['diff'] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result['n'] for result in results)
    conjecture_holds = all(result['diff'] <= 1e-6 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symplectic_capacity_diff",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if "metric_value" not in r or r["metric_value"] is None), None)
        print(f"RESULT: INCONCLUSIVE reason=missing_data first_failing_seed={first_failing_seed}")