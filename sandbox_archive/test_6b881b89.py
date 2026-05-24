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
    
    def generate_ac0_parity_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def evaluate_function(f, x):
        result = f[0]
        for i in range(1, len(f)):
            if f[i] == 1:
                result ^= x[i-1]
        return result
    
    def p_adic_log(x, p):
        if x <= 0:
            return float('-inf')
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        s = len(generate_ac0_parity_circuit(n))
        min_value = float('inf')
        
        for _ in range(30):
            f = generate_ac0_parity_circuit(n)
            x = [random.choice([0, 1]) for _ in range(n)]
            value = evaluate_function(f, x)
            if abs(value) < min_value:
                min_value = abs(value)
        
        p_adic_val = p_adic_log(min_value, 2)
        results.append((s, p_adic_val))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_ranks = {x[i]: i + 1 for i in range(n)}
        y_ranks = {y[i]: i + 1 for i in range(n)}
        
        sum_differences_squared = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        rho = 1 - (6 * sum_differences_squared) / (n * (n**2 - 1))
        return rho
    
    x, y = zip(*results)
    rho = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.7,
        "counterexample": "" if rho >= 0.7 else f"Spearman's rank correlation coefficient {rho} < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_rho = sum(res["metric_value"] for res in results) / len(results)
        std_rho = math.sqrt(sum((res["metric_value"] - mean_rho) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")