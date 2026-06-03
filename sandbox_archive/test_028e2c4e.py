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
    
    def generate_kcnf(n, k):
        cnf = []
        for _ in range(k * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        return cnf
    
    def is_valid_clause(clause, assignment):
        return any(assignment[abs(lit) - 1] * lit > 0 for lit in clause)
    
    def evaluate_cnf(cnf, assignment):
        return all(is_valid_clause(clause, assignment) for clause in cnf)
    
    def find_automorphisms(cnf):
        n = len(cnf)
        automorphisms = []
        for perm in itertools.permutations(range(n)):
            if all(evaluate_cnf(cnf, {perm[i] + 1: val for i, val in enumerate(assignment)}) for assignment in itertools.product([-1, 1], repeat=n)):
                automorphisms.append(perm)
        return automorphisms
    
    def communication_complexity_rank(cnf):
        n = len(cnf)
        max_rank = 0
        for perm in itertools.permutations(range(n)):
            rank = 0
            for clause in cnf:
                if all(perm[abs(lit) - 1] * lit > 0 for lit in clause):
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_kcnf(n, k=3)
            automorphisms = find_automorphisms(cnf)
            order = len(automorphisms)
            rank = communication_complexity_rank(cnf)
            
            if order < n**2 * math.log(n):
                conjecture_holds = False
                counterexample = f"n={n}, |Aut(φ)|={order}, r(φ)={rank}"
            
            total_metric_value += order
            instances_tested += 1
            n_max = max(n_max, n)
    
    return {
        "metric_name": "Order of Automorphism Group",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")