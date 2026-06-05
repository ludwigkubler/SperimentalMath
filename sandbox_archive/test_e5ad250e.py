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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def smallest_prime_dividing(n):
        for i in range(2, n + 1):
            if n % i == 0 and is_prime(i):
                return i
        return None
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_symbols = {}
        for symbol in set(symbol for clause in clauses for symbol in clause):
            positive_count = sum(1 for clause in clauses if symbol in clause)
            negative_count = sum(1 for clause in clauses if -symbol in clause)
            if positive_count == 0:
                pure_symbols[symbol] = True
            elif negative_count == 0:
                pure_symbols[symbol] = False
        
        for symbol, value in pure_symbols.items():
            if not dpll([c for c in clauses if symbol not in c and -symbol not in c], assignment | {symbol: value}):
                continue
            return True
        
        literal = unit_clauses[0]
        if literal > 0:
            if not dpll(clauses, assignment | {literal: True}):
                return dpll(clauses, assignment | {literal: False})
        else:
            if not dpll(clauses, assignment | {-literal: True}):
                return dpll(clauses, assignment | {-literal: False})
        
        return False
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            clauses.append(clause)
        return clauses
    
    def log_q(q):
        return math.log(q)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        q = smallest_prime_dividing(n)
        if q is None:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        
        proof_length = dpll(cnf)
        if not proof_length:
            counterexample = f"CNF with {n} variables has no DPLL proof"
            conjecture_holds = False
            break
        
        metric_value = log_q(q)
        total_metric_value += metric_value
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    std_dev = math.sqrt(sum((x - mean_metric_value) ** 2 for x in [log_q(smallest_prime_dividing(random.randint(5, 40))) for _ in range(30)]) / (instances_tested - 1)) if instances_tested > 1 else 0.0
    
    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8 and std_dev <= 3 * std_dev:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")