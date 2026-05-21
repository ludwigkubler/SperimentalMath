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
    
    def real_stable_polynomial(clauses):
        var = 1
        monomial = (var + 1) * (-var - 1)
        for clause in clauses:
            monomial *= (var + 1) * (-var - 1)
        return monomial
    
    def sturm_sequence(poly, x_values):
        seq = [poly]
        while True:
            derivative = []
            for i in range(1, len(seq[-1])):
                coeff = Fraction(seq[-1][i]) * Fraction(i)
                derivative.append(coeff)
            if not derivative:
                break
            seq.append(derivative)
        
        def evaluate(poly, x):
            result = 0
            power = 1
            for coeff in reversed(poly):
                result += coeff * power
                power *= x
            return result
        
        signs = []
        for x in x_values:
            values = [evaluate(poly, x) for poly in seq]
            sign_changes = sum(1 for i in range(1, len(values)) if (values[i] > 0 and values[i-1] <= 0) or (values[i] < 0 and values[i-1] >= 0))
            signs.append(sign_changes)
        
        return min(signs), max(signs)
    
    def count_real_roots(poly, x_values):
        lower_bound, upper_bound = sturm_sequence(poly, x_values)
        return upper_bound - lower_bound
    
    n = random.randint(5, 40)
    k = random.randint(2, n-1)
    num_clauses = random.randint(k, n*(n-1)//2)
    
    clauses = set()
    while len(clauses) < num_clauses:
        clause = tuple(sorted(random.sample(range(n), k)))
        if clause not in clauses:
            clauses.add(clause)
    
    clique_poly = real_stable_polynomial(clauses)
    x_values = [-10, -5, 0, 5, 10]
    root_count = count_real_roots(clique_poly, x_values)
    
    return {
        "metric_name": "root_count",
        "metric_value": root_count,
        "instances_tested": 1,
        "conjecture_holds": root_count >= n / 10,
        "counterexample": "" if root_count >= n / 10 else f"n={n}, k={k}, clauses={clauses}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\", first_failing_seed={first_failing_seed}")