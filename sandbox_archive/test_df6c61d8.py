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

def generate_random_formula(n, c):
    clauses = []
    for _ in range(c):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = -clause[0], -clause[1]
        clauses.append(clause)
    return clauses

def is_disjoint(S1, S2):
    for s1 in S1:
        for s2 in S2:
            if abs(s1) == abs(s2):
                return False
    return True

def matroid_rank(clauses):
    rank = 0
    selected_clauses = []
    for clause in clauses:
        if all(not is_disjoint(clause, sc) for sc in selected_clauses):
            selected_clauses.append(clause)
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    c = n**2
    formula = generate_random_formula(n, c)
    
    rank = matroid_rank(formula)
    k_clique_rank = max(rank for clause in formula if len(clause) == 3)
    
    metric_name = "Matroid Rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n >= 3 and k_clique_rank >= 0.4 * n:
        conjecture_holds = True
    elif n < 3 or k_clique_rank <= 5 * math.log(n):
        conjecture_holds = True
    else:
        counterexample = "k-CLIQUE instance with rank not meeting expected bounds"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r['counterexample'] for r in results):
        counterexample = next(r['counterexample'] for r in results if r['counterexample'])
        first_failing_seed = next(r['seed'] for r in results if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")