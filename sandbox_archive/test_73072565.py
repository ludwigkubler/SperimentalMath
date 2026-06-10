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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def incidence_algebra(clauses):
        n = len(clauses[0])
        I = [[0] * (2**n) for _ in range(2**n)]
        for i in range(1, 2**n):
            for j in range(i + 1, 2**n):
                if all((i & (1 << k)) or (j & (1 << k)) for k in range(n)):
                    I[i][j] = 1
                    I[j][i] = 1
        return I
    
    def twisted_module_order(I):
        n = len(I)
        order = 0
        while True:
            found = False
            for i in range(1, n):
                if all(I[i][j] == 0 for j in range(n) if j != i):
                    order += 1
                    I[i][:] = [0] * n
                    I[:][i] = [0] * n
                    found = True
            if not found:
                break
        return order
    
    def dpll_search_tree_height(clauses):
        def backtrack(model, clause_index):
            if clause_index == len(clauses):
                return 1
            clause = clauses[clause_index]
            for literal in clause:
                new_model = model[:]
                new_model[literal - 1] = True
                if all(new_model[i - 1] or not (i & literal) for i in range(1, len(clauses) + 1)):
                    height = backtrack(new_model, clause_index + 1)
                    if height > max_height:
                        max_height = height
            return max_height
        
        max_height = 0
        backtrack([False] * len(clauses[0]), 0)
        return max_height
    
    def pearson_correlation(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        cov = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n)) / n
        var1 = sum((values1[i] - mean1) ** 2 for i in range(n)) / n
        var2 = sum((values2[i] - mean2) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var1) * math.sqrt(var2))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        phi = generate_sat_instance(n)
        I = incidence_algebra(phi)
        min_order = twisted_module_order(I)
        height = dpll_search_tree_height(phi)
        results.append((min_order, height))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    values1, values2 = zip(*results)
    correlation = pearson_correlation(values1, values2)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.8 or all(abs(corr) < 0.5 for corr in results),
        "counterexample": "" if abs(correlation) >= 0.8 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8 or all(abs(corr) < 0.5 for corr in results)) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) < 0.5 for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if abs(r['metric_value']) < 0.5)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")