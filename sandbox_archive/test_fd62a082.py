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
    
    def generate_cnf(k, m):
        variables = list(range(1, k + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(1, k))]
            clauses.append(clause)
        return clauses
    
    def cnf_to_var(cnf):
        var_set = set()
        for clause in cnf:
            for lit in clause:
                var_set.add(abs(lit))
        return sorted(var_set)
    
    def cnf_to_poly(cnf, vars):
        n = len(vars)
        poly = [0] * (1 << n)
        for clause in cnf:
            term = 1
            for lit in clause:
                if lit > 0:
                    term *= (1 - vars[lit-1])
                else:
                    term *= (vars[-lit-1])
            poly[sum(1 << (vars.index(abs(lit)) - 1) for lit in clause)] += term
        return poly
    
    def p_adic_hodge_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            if poly[i] != 0:
                rank += 1
        return rank
    
    def clause_complexity(cnf):
        return sum(len(clause) for clause in cnf)
    
    k_values = [3, 4, 5]
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for k in k_values:
        for m in m_values:
            cnf = generate_cnf(k, m)
            vars = cnf_to_var(cnf)
            poly = cnf_to_poly(cnf, vars)
            rank = p_adic_hodge_rank(poly)
            complexity = clause_complexity(cnf)
            results.append((rank, complexity))
    
    if not results:
        return {
            "metric_name": "p-adic Hodge Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r for r, _ in results]
    complexities = [c for _, c in results]
    mean_rank = sum(ranks) / len(ranks)
    mean_complexity = sum(complexities) / len(complexities)
    std_rank = math.sqrt(sum((r - mean_rank) ** 2 for r in ranks) / len(ranks))
    std_complexity = math.sqrt(sum((c - mean_complexity) ** 2 for c in complexities) / len(complexities))
    
    correlation_coefficient = sum((ranks[i] - mean_rank) * (complexities[i] - mean_complexity) for i in range(len(ranks))) / (len(ranks) * std_rank * std_complexity)
    
    return {
        "metric_name": "p-adic Hodge Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and abs(mean_rank - mean_complexity) <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient: {correlation_coefficient}, Mean difference: {abs(mean_rank - mean_complexity)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")