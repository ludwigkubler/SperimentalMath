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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        depth = 0
        for clause in cnf:
            depth += abs(sum(1 for lit in clause if lit > 0))
        return depth
    
    def monomial_representation(cnf):
        variables = set(abs(lit) for clause in cnf for lit in clause)
        n_vars = len(variables)
        monomials = []
        for i in range(2**n_vars):
            monomial = [1 if (i >> j) & 1 else -1 for j in range(n_vars)]
            if all(any(monomial[abs(lit)-1] * lit >= 0 for lit in clause) for clause in cnf):
                monomials.append(monomial)
        return len(monomials)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            depth = frege_proof_depth(cnf)
            if depth == 0:
                continue
            instances_tested += 1
            metric_value = monomial_representation(cnf) / math.log(depth + 1, 2)
            total_metric_value += metric_value
            if metric_value <= 0.5:
                conjecture_holds = False
                counterexample = f"n={n}, depth={depth}, monomials={monomial_representation(cnf)}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = (instances_tested - sum(1 for _ in range(instances_tested) if metric_value <= 0.5)) / instances_tested
    
    return {
        "metric_name": "Monomial Representation Size",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] > 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NOT_APPLICABLE support_fraction={support_fraction}")
    elif any(r["metric_value"] <= 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] <= 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")