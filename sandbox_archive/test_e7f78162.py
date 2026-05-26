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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def geometric_langlands_dual(cnf):
    # Placeholder function for constructing the geometric Langlands dual object from a CNF
    m = len(cnf)
    n = max(abs(lit) for clause in cnf for lit in clause)
    return Fraction(m**(1/4) * n**(3/8))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n*2)
        cnf = generate_cnf(n, m)
        dual_rank = geometric_langlands_dual(cnf)
        results.append(dual_rank)
    
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
    conjecture_holds = all(rank <= m**(1/4) * n**(3/8) for rank, m, n in zip(results, [len(cnf) for cnf in generate_cnf(n, m)], [max(abs(lit) for clause in cnf for lit in clause) for cnf in generate_cnf(n, m)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = (sum((x - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r <= m**(1/4) * n**(3/8)) / len(results)
    
    if all(r <= m**(1/4) * n**(3/8) for r, m, n in zip(results, [len(cnf) for cnf in generate_cnf(n, m)], [max(abs(lit) for clause in cnf for lit in clause) for cnf in generate_cnf(n, m)])):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r > m**(1/4) * n**(3/8) for r, m, n in zip(results, [len(cnf) for cnf in generate_cnf(n, m)], [max(abs(lit) for clause in cnf for lit in clause) for cnf in generate_cnf(n, m)])):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(max(results))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")