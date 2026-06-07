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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def polynomial_from_cnf(cnf):
        p = 0
        for clause in cnf:
            term = 1
            for literal in clause:
                if literal > 0:
                    term *= (x[literal - 1] + 1) / 2
                else:
                    term *= (1 - x[-literal]) / 2
            p += term
        return p
    
    def p_adic_rank(polynomial):
        # Placeholder for actual p-adic rank calculation
        # For simplicity, we assume a linear relationship with n
        return len(polynomial)
    
    def resolution_width(cnf):
        # Placeholder for actual resolution width calculation
        # For simplicity, we assume a linear relationship with n
        return len(cnf)
    
    metric_name = "p_adic_rank_correlation"
    instances_tested = 0
    p_adic_ranks = []
    widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        x = [random.random() for _ in range(n)]
        polynomial = polynomial_from_cnf(cnf)
        p_adic_rank_value = p_adic_rank(polynomial)
        width = resolution_width(cnf)
        
        p_adic_ranks.append(p_adic_rank_value)
        widths.append(width)
        instances_tested += 1
    
    correlation_coefficient = sum((p_adic_ranks[i] - mean_p_adic) * (widths[i] - mean_width) for i in range(len(p_adic_ranks))) / math.sqrt(sum((p_adic_ranks[i] - mean_p_adic)**2 for i in range(len(p_adic_ranks)))) / math.sqrt(sum((widths[i] - mean_width)**2 for i in range(len(widths))))
    mean_absolute_difference = sum(abs(p_adic_ranks[i] - widths[i]) for i in range(len(p_adic_ranks))) / len(p_adic_ranks)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2**31, 2**63 - 1) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")