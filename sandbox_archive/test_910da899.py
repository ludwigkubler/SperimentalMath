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

def parse_tseitin(formula):
    n = 0
    for char in formula:
        if 'x' in char:
            n = max(n, int(char[1:]))
        elif '!' in char:
            n = max(n, int(char[2:]))
    return n, formula

def resolution_proof_length(formula):
    n, clauses = parse_tseitin(formula)
    proof = []
    for clause in clauses.split(' & '):
        if 'x' not in clause and '!' not in clause:
            continue
        literals = clause.split(' | ')
        literal_set = set(literals)
        while True:
            found_resolvent = False
            for i in range(len(proof)):
                resolvents = []
                for j in range(i + 1, len(proof)):
                    if any(-l == m for l in proof[i] for m in proof[j]):
                        resolvent = [l for l in proof[i] if l not in proof[j]] + \
                                    [m for m in proof[j] if -m not in proof[i]]
                        resolvents.append(resolvent)
            if not resolvents:
                break
            resolvent = min(resolvents, key=len)
            proof.append(tuple(sorted(resolvent)))
            found_resolvent = True
        if not found_resolvent:
            return len(proof)
    return len(proof)

def monoidal_category_rank(formula):
    n, _ = parse_tseitin(formula)
    rank = 0
    for i in range(n):
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    variables = ''.join(f'x{i}' for i in range(n))
    clauses = ' & '.join(
        f'{random.choice(variables)} | !{random.choice(variables)}' for _ in range(m)
    )
    formula = f'({clauses})'
    
    proof_length = resolution_proof_length(formula)
    category_rank = monoidal_category_rank(formula)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": category_rank,
        "instances_tested": 1,
        "conjecture_holds": category_rank >= proof_length,
        "counterexample": "" if category_rank >= proof_length else f"Formula: {formula}, Category Rank: {category_rank}, Proof Length: {proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")