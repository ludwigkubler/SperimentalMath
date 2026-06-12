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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        mte = [sum(f[i:i+n] == f[j:j+n] for j in range(len(f))) / (len(f) - n + 1) for i in range(n)]
        mean_mte = sum(mte) / n
        return sum((x - mean_mte)**2 for x in mte) / n
    
    def alexander_orlik_solomon_invariant(f):
        n = len(f)
        if n == 1:
            return f[0]
        alpha_omega = 0
        for i in range(1, n + 1):
            sub_f = [f[j] for j in range(n) if (j & (i - 1)) != 0]
            alpha_omega += sum(sub_f) * (-1)**(n - i)
        return abs(alpha_omega)
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return covariance / (std_dev_x * std_dev_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        alpha_omega_values = []
        rc_values = []
        for _ in range(30):
            f = generate_random_boolean_function(n)
            alpha_omega = alexander_orlik_solomon_invariant(f)
            rc = communication_complexity_rank_variance(f)
            alpha_omega_values.append(alpha_omega)
            rc_values.append(rc)
            instances_tested += 1
        correlation_coefficient = pearson_correlation_coefficient(alpha_omega_values, rc_values)
        results.append({
            "n": n,
            "alpha_omega_mean": sum(alpha_omega_values) / len(alpha_omega_values),
            "rc_mean": sum(rc_values) / len(rc_values),
            "correlation_coefficient": correlation_coefficient
        })
    
    alpha_omega_mean = sum(result["alpha_omega_mean"] for result in results) / len(results)
    rc_mean = sum(result["rc_mean"] for result in results) / len(results)
    correlation_coefficient = sum(result["correlation_coefficient"] for result in results) / len(results)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(result["correlation_coefficient"] >= 0.5 for result in results),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 157))[:30]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")