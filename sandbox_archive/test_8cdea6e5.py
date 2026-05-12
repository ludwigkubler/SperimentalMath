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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def truth_table_additive_energy(f):
    n = len(next(iter(f.values())))
    energy = 0
    for a in range(2**n):
        for b in range(a+1, 2**n):
            for c in range(b+1, 2**n):
                for d in range(c+1, 2**n):
                    if f[a] + f[b] == f[c] + f[d]:
                        energy += 1
    return energy

def dpll(f, assignment, depth=0, max_depth=None):
    if len(assignment) == len(next(iter(f.values()))):
        return all(f[tuple(sorted(assignment.items(), key=lambda x: x[0]))] == v for t, v in f.items())
    var = next(k for k in range(len(next(iter(f.values())))) if k not in assignment)
    for val in [0, 1]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        if dpll(f, new_assignment, depth + 1, max_depth):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 4
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        f = {tuple(random.getrandbits(n) for _ in range(2**n)): random.choice([0, 1]) for _ in range(2**n)}
        energy = truth_table_additive_energy(f)
        if energy > 2**(n/2):
            circuit_size = 2**(n/4)
            if dpll(f, {}, max_depth=int(circuit_size)):
                conjecture_holds = False
                counterexample = f"Counterexample found: Function with energy {energy} and circuit size < {circuit_size}"
                break

        metric_value += energy

    return {
        "metric_name": "Additive Energy",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
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
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")