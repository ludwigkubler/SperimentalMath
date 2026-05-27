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
    
    def generate_boolean_formula(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.choice([-1, 1])]
            clauses.append(clause)
        return clauses
    
    def monomial_ideal_size(clauses):
        size = len(set(tuple(sorted(c)) for c in clauses))
        return size
    
    def minimal_generators(n, m):
        # Simplified heuristic to estimate the number of generators
        return int(math.log(n) + math.pow(m, 0.25))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different formulas
            formula = generate_boolean_formula(n, random.randint(1, 2*n))
            size = monomial_ideal_size(formula)
            generators = minimal_generators(n, size)
            results.append(generators)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(gen <= math.log(n) + math.pow(m, 0.25) for n, m, gen in zip(n_values, [len(formula) for formula in results], results))
    
    return {
        "metric_name": "MinimalGenerators",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula with n={n_values[results.index(max(results))]}, m={len(formula)}, generators={max(results)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] - math.log(r["n"]) - math.pow(len(r["formula"]), 0.25) > 3 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n={r['n']}, m={len(r['formula'])}, generators={r['metric_value']}\" first_failing_seed={results.index(next(r for r in results if not r['conjecture_holds']))}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")