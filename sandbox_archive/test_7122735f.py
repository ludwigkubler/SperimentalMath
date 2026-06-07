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
    
    def cnf_to_polynomial(cnf):
        n = len(cnf[0])
        polynomial = [0] * (2 ** n)
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal < 0:
                    term *= -polynomial[-literal]
                else:
                    term *= polynomial[literal]
            polynomial[term] += 1
        return polynomial
    
    def resolution_width(cnf):
        n = len(cnf[0])
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if not clause:
                return 0
            literal = clause[0]
            new_clauses = []
            for other_clause in queue:
                if literal in other_clause:
                    new_clause = tuple(sorted(set(other_clause) - {literal}))
                    if new_clause:
                        new_clauses.append(new_clause)
                elif -literal in other_clause:
                    new_clause = tuple(sorted(set(other_clause) | {literal}))
                    if new_clause:
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return len(queue)
    
    def p_adic_rank(polynomial):
        rank = 0
        for coeff in polynomial:
            if coeff != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_p_adic_rank = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = [[random.randint(-n, n) for _ in range(n)] for _ in range(random.randint(1, n))]
            polynomial = cnf_to_polynomial(cnf)
            width = resolution_width(cnf)
            p_adic_rank_value = p_adic_rank(polynomial)
            
            total_p_adic_rank += p_adic_rank_value
            total_width += width
            instances_tested += 1
    
    mean_p_adic_rank = total_p_adic_rank / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(p_adic_rank_value * width for p_adic_rank_value, width in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_p_adic_rank * mean_width) / math.sqrt((instances_tested * sum(p_adic_rank_value ** 2 for p_adic_rank_value in range(instances_tested)) - instances_tested * mean_p_adic_rank ** 2) * (instances_tested * sum(width ** 2 for width in range(instances_tested)) - instances_tested * mean_width ** 2))
    
    mean_abs_diff = sum(abs(p_adic_rank_value - width) for p_adic_rank_value, width in zip(range(instances_tested), range(instances_tested))) / instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8 or mean_abs_diff>3"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")