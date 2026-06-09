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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses

    def dpll(model, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            model[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(model, new_clauses)
        pure_literal = next((v for v in variables if all(v not in c or not model.get(-v) for c in clauses)), None)
        if pure_literal:
            model[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(model, new_clauses)
        literal = random.choice(variables)
        model[literal] = True
        if dpll(model.copy(), [c for c in clauses if literal not in c]):
            return True
        model[-literal] = True
        return dpll(model, [c for c in clauses if -literal not in c])

    def frege_proof_depth(clauses):
        return len(dpll({}, clauses))

    def regular_expression_minimization(cnf):
        # Placeholder for actual minimization algorithm
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_r = 0
    total_d = 0

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, int(1.5 * n))
            r = regular_expression_minimization(cnf)
            d = frege_proof_depth(cnf)
            instances_tested += 1
            total_r += r
            total_d += d

    if instances_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_r = total_r / instances_tested
    mean_d = total_d / instances_tested

    # Placeholder for Pearson correlation coefficient calculation
    covariance = sum((r - mean_r) * (d - mean_d) for r, d in zip(r_values, d_values)) / instances_tested
    variance_r = sum((r - mean_r) ** 2 for r in r_values) / instances_tested
    variance_d = sum((d - mean_d) ** 2 for d in d_values) / instances_tested
    pearson_corr = covariance / (math.sqrt(variance_r) * math.sqrt(variance_d))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.7 and pearson_corr <= -0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")