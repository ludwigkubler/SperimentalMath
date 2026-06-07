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
    
    def generate_k_clique(k, n):
        if k > n or k <= 0:
            return None
        vertices = list(range(n))
        clique = set(random.sample(vertices, k))
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in clique and (j, i) not in clique:
                    return None
        return clique
    
    def hodge_index(clique):
        n = len(clique)
        if n == 0:
            return 0
        return Fraction(n * (n - 1), 2)
    
    def communication_complexity_rank_variance(clique):
        n = len(clique)
        if n == 0:
            return 0
        return Fraction(n * (n - 1) * (n - 2) * (n - 3), 24)
    
    k_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_hodge_index = 0
    total_variance = 0
    
    for n in range(5, 41):
        for _ in range(5):  # Ensure at least 5 instances per size
            clique = generate_k_clique(random.randint(2, min(n, 6)), n)
            if clique is None:
                continue
            hodge = hodge_index(clique)
            variance = communication_complexity_rank_variance(clique)
            total_hodge_index += hodge
            total_variance += variance
            instances_tested += 1
    
    mean_hodge_index = Fraction(total_hodge_index, instances_tested)
    mean_variance = Fraction(total_variance, instances_tested)
    
    correlation_coefficient = (instances_tested * mean_hodge_index * mean_variance - 
                               total_hodge_index * total_variance) / (
        math.sqrt(instances_tested * (total_hodge_index**2 - mean_hodge_index**2)) *
        math.sqrt(instances_tested * (total_variance**2 - mean_variance**2))
    )
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient > 0.8 and correlation_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")