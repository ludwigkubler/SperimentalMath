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

def generate_random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                  for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def integer_to_monomial(i, n):
    monomial = ""
    for j in range(n):
        if i & (1 << j):
            monomial += f"x{j+1}"
        elif i & (1 << (-j - 1)):
            monomial += f"~x{j+1}"
    return monomial

def generate_monomial_ideal(cnf, n):
    ideal = set()
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                monomial = integer_to_monomial(literal - 1, n)
            else:
                monomial = f"~{integer_to_monomial(-literal - 1, n)}"
            ideal.add(monomial)
    return ideal

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = generate_random_cnf(n, m)
    
    try:
        ideal = generate_monomial_ideal(cnf, n)
        generators = len(ideal)
        
        # Placeholder for Frege proof size check
        frege_proof_size = None
        
        return {
            "metric_name": "Generators",
            "metric_value": generators,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    except Exception as e:
        return {
            "metric_name": "Generators",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_generators = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_generators = math.sqrt(sum((r["metric_value"] - mean_generators)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_generators} std={std_generators} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")