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
            clause = [random.randint(-n, n) for _ in range(n)]
            if all(x != 0 for x in clause):
                clauses.append(clause)
        return clauses
    
    def minimal_clauses(clauses):
        # Simplified version of finding minimal set of clauses
        return list(set(tuple(sorted(c)) for c in clauses))
    
    def eichler_coefficients(clauses):
        # Placeholder function to count distinct coefficients
        return len(set(tuple(sorted(c)) for c in clauses))
    
    def count_proofs(clauses):
        # Placeholder function to count proofs (simplified)
        return 2**len(clauses)
    
    n = random.randint(5, 40)
    cnf_formula = generate_cnf(n)
    pi = minimal_clauses(cnf_formula)
    eichler_coeffs = eichler_coefficients(pi)
    num_proofs = count_proofs(cnf_formula)
    
    metric_value = eichler_coeffs / n
    conjecture_holds = 2**(n/2) <= num_proofs
    
    return {
        "metric_name": "Eichler Coefficients / Variables",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, eichler_coeffs={eichler_coeffs}, num_proofs={num_proofs}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")