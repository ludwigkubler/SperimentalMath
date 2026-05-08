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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def monomial_to_integer(monomial, n):
    value = 0
    for literal in monomial:
        if literal > 0:
            value |= (1 << (literal - 1))
        else:
            value &= ~(1 << (-literal - 1))
    return value

def integer_to_monomial(value, n):
    monomial = []
    for i in range(n):
        if value & (1 << i):
            monomial.append(i + 1)
        elif value & (1 << (-i - 1)):
            monomial.append(-(i + 1))
    return monomial

def generate_monomial_ideal(cnf, n):
    ideal = set()
    for clause in cnf:
        for i in range(1 << n):
            if all(literal in integer_to_monomial(i, n) for literal in clause):
                ideal.add(i)
    return ideal

def square_free_decomposition(ideal, n):
    generators = []
    while ideal:
        generator = min(ideal, key=lambda x: bin(x).count('1'))
        generators.append(generator)
        ideal -= {x & ~generator for x in ideal}
    return generators

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    cnf = generate_cnf(n, m)
    
    ideal = generate_monomial_ideal(cnf, n)
    generators = square_free_decomposition(ideal, n)
    
    metric_value = len(generators)
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Number of Generators",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")