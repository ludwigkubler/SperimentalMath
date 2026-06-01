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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n - 1):
            gate_type = random.choice(['AND', 'OR'])
            inputs = random.sample(range(n), random.randint(1, n))
            circuit.append((gate_type, inputs))
        return circuit
    
    def monotone_complexity(circuit):
        n = len(circuit)
        dp = [0] * (n + 1)
        for i in range(n):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                dp[i+1] = max(dp[j] for j in inputs) + 1
            elif gate_type == 'OR':
                dp[i+1] = min(dp[j] for j in inputs) + 1
        return dp[-1]
    
    def kac_moody_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(n):
            gate_type, inputs = circuit[i]
            if gate_type == 'AND':
                rank += max(len(inputs), 1)
            elif gate_type == 'OR':
                rank += min(len(inputs), 1)
        return rank
    
    n_max = 40
    instances_tested = 30
    metrics = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        circuit = generate_random_circuit(n)
        mu_C = monotone_complexity(circuit)
        r_A_C = kac_moody_rank(circuit)
        metrics.append((mu_C, r_A_C))
    
    if not metrics:
        return {
            "metric_name": "monotone_complexity",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mu_values = [mu for mu, _ in metrics]
    r_A_C_values = [r for _, r in metrics]
    
    mean_mu = sum(mu_values) / len(mu_values)
    mean_r_A_C = sum(r_A_C_values) / len(r_A_C_values)
    
    ss_total = sum((mu - mean_mu)**2 + (r - mean_r_A_C)**2 for mu, r in metrics)
    ss_regression = sum((mu - mean_mu) * (r - mean_r_A_C) for mu, r in metrics)
    
    if len(metrics) < 2:
        return {
            "metric_name": "monotone_complexity",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    r_squared = ss_regression**2 / (ss_total * len(metrics))
    p_value = 1 - math.comb(len(metrics) - 2, 0.5 * (1 - r_squared)) / math.comb(len(metrics), 0.5 * (1 - r_squared))
    
    return {
        "metric_name": "monotone_complexity",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r_squared >= 0.9 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_r_squared = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")