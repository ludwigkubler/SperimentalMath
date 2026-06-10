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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        circuit_ranks = []
        for k in range(1, n+1):
            rank = 0
            for i in range(n):
                if f[i] == 1:
                    rank += 1
            circuit_ranks.append(rank)
        return sum((x - sum(circuit_ranks) / len(circuit_ranks))**2 for x in circuit_ranks) / len(circuit_ranks)
    
    def homogeneous_polynomials(n, d):
        if n == 0:
            return [[1]]
        polynomials = []
        for i in range(d+1):
            for p in homogeneous_polynomials(n-1, d-i):
                polynomials.append([i] + p)
        return polynomials
    
    def hodge_class_representation(f, polynomials):
        n = len(f)
        H = []
        for p in polynomials:
            if sum(p[i] * f[i] for i in range(n)) == 0:
                H.append(p)
        return H
    
    def dim_H(H):
        rank = 0
        while H:
            v = H.pop()
            rank += 1
            H = [h for h in H if any(h[j] != v[j] for j in range(len(v)))]
        return rank
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_random_boolean_function(n)
        R_f = communication_complexity_rank_variance(f)
        polynomials = homogeneous_polynomials(n, n)
        H_f = hodge_class_representation(f, polynomials)
        dim_H_f = dim_H(H_f)
        
        metric_values.append(dim_H_f)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        mean_R_f = sum(communication_complexity_rank_variance(generate_random_boolean_function(n)) for n in range(5, n_max+1)) / (n_max - 4)
        numerator = sum((metric_values[i] - mean_value) * (communication_complexity_rank_variance(generate_random_boolean_function(i+5)) - mean_R_f) for i in range(len(metric_values)))
        denominator = math.sqrt(sum((x - mean_value)**2 for x in metric_values)) * math.sqrt(sum((communication_complexity_rank_variance(generate_random_boolean_function(i+5)) - mean_R_f)**2 for i in range(n_max-4)))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_rank_variance",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")