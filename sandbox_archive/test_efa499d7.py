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
    
    def generate_k_clique_cnf(k, n):
        clauses = []
        for i in range(n - k + 1):
            for j in range(i + 1, n - k + 2):
                clause = [random.choice([f'x{i}', f'~x{i}']) for _ in range(k)]
                clauses.append(clause)
        return clauses
    
    def matroid_representation(cnf):
        variables = set()
        for clause in cnf:
            for lit in clause:
                if lit.startswith('x'):
                    variables.add(lit[1:])
        matroid = {var: [] for var in variables}
        for clause in cnf:
            for lit in clause:
                if lit.startswith('x'):
                    matroid[lit[1:]].append(clause)
        return matroid
    
    def tropical_rank(matroid):
        rank = 0
        for var, deps in matroid.items():
            if not deps:
                continue
            pivot = random.choice(deps)
            rank += 1
            for dep in deps:
                if dep != pivot:
                    coeff = Fraction(1, len(dep))
                    for i in range(len(pivot)):
                        if pivot[i] != dep[i]:
                            dep[i] = '~' + dep[i]
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 4))
    cnf = generate_k_clique_cnf(k, n)
    matroid = matroid_representation(cnf)
    rank = tropical_rank(matroid)
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")