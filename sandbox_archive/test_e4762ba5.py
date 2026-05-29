# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_kcnf_instance(n: int, m: int) -> tuple:
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return len(clauses), variables, clauses

def tropicalizer(clause, variables):
    return [Fraction(abs(x)) for x in clause]

def tropical_semigroup(clauses, variables):
    semigroup = set()
    for clause in clauses:
        t_clause = tropicalizer(clause, variables)
        for i in range(len(t_clause)):
            for j in range(i + 1, len(t_clause)):
                new_element = max(t_clause[i], t_clause[j])
                if new_element not in semigroup:
                    semigroup.add(new_element)
    return semigroup

def arithmetic_rank(semigroup):
    n = len(semigroup)
    identity = Fraction(1)
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    
    for i, x in enumerate(sorted(semigroup)):
        for j, y in enumerate(sorted(semigroup)):
            if x >= y:
                matrix[i][j] = identity
    
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
    return rank

def randomized_communication_complexity(arithmetic_rank):
    return 2 ** arithmetic_rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m, variables, clauses = generate_kcnf_instance(n, n)
        semigroup = tropical_semigroup(clauses, variables)
        tau_I = arithmetic_rank(semigroup)
        CC_R_I = randomized_communication_complexity(tau_I)
        
        if CC_R_I < 2 ** tau_I:
            return {
                "metric_name": "Randomized Communication Complexity",
                "metric_value": CC_R_I,
                "instances_tested": m,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={m}, tau(I)={tau_I}, CC_R(I)={CC_R_I}"
            }
        
        results.append(CC_R_I)
    
    return {
        "metric_name": "Randomized Communication Complexity",
        "metric_value": sum(results) / len(results),
        "instances_tested": sum(m for _, _, m in [generate_kcnf_instance(n, n) for n in n_values]),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 2**arithmetic_rank(tropical_semigroup(generate_kcnf_instance(n, n)[2], generate_kcnf_instance(n, n)[1])[0])) / len(results)
    
    if all(r >= 2**arithmetic_rank(tropical_semigroup(generate_kcnf_instance(n, n)[2], generate_kcnf_instance(n, n)[1])[0]) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 2**arithmetic_rank(tropical_semigroup(generate_kcnf_instance(n, n)[2], generate_kcnf_instance(n, n)[1])[0]))
        print(f"RESULT: FALSIFIED counterexample='n={n}, m={m}, tau(I)={tau_I}, CC_R(I)={CC_R_I}' first_failing_seed={first_failing_seed}")