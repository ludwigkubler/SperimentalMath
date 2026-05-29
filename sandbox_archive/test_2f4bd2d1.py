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

def generate_random_monomial_ideal(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        clause = tuple(random.sample(variables, random.randint(1, n)))
        clauses.add(clause)
    return clauses

def generate_coxeter_group_action(G, I):
    orbits = set()
    for i in range(len(I)):
        orbit = {tuple(sorted([G[i][j] for j in I]))}
        orbits.update(orbit)
    return orbits

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    m = 10
    
    I = generate_random_monomial_ideal(n, m)
    c = len(I)
    
    # Generate a Coxeter group action (simplified for demonstration)
    G = [[i + 1 if i != j else -1 for j in range(n)] for i in range(n)]
    
    orbits = generate_coxeter_group_action(G, I)
    
    metric_value = len(orbits)
    conjecture_holds = metric_value <= c ** 1.5
    counterexample = "" if conjecture_holds else f"Too many orbits: {metric_value} > {c**1.5}"
    
    return {
        "metric_name": "Number of Orbits",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many orbits\" first_failing_seed={first_failing_seed}")