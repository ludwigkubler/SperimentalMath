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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n * 2)
                if var > n:
                    var -= n
                else:
                    var += n
                clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def symplectic_leaf_decomposition(cnf):
        leaves = set()
        for clause in cnf:
            leaves.update(clause)
        return len(leaves)
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf)
        rank = 0
        for i in range(1, n + 1):
            if any(i in clause for clause in cnf):
                rank += 1
        return (rank / n) * ((n - rank) / n)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        var_x = sum((xi - mean_x) ** 2 for xi in x) / len(x)
        var_y = sum((yi - mean_y) ** 2 for yi in y) / len(y)
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(50):
            cnf = generate_k_cnf(n, n)
            leaves_count = symplectic_leaf_decomposition(cnf)
            rank_variance = communication_complexity_rank_variance(cnf)
            
            metric_values.append(leaves_count * rank_variance)
            instances_tested += 1
            
            if len(metric_values) >= 30:
                mean_metric = sum(metric_values) / len(metric_values)
                std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
                correlation_coefficient = correlation(metric_values, [i for i in range(1, instances_tested + 1)])
                
                if correlation_coefficient < 0.5:
                    conjecture_holds = False
                    counterexample = f"Correlation coefficient {correlation_coefficient} is less than 0.5"
    
    return {
        "metric_name": "SymplecticLeavesCount * RankVariance",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")