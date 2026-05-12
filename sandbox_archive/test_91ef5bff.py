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
    n = int(f.keys()[0].bit_length())
    energy = 0
    for a in range(2**n):
        for b in range(a, 2**n):
            for c in range(b, 2**n):
                d = (a + b - c) % (2**n)
                if f[a] + f[b] == f[c] + f[d]:
                    energy += 1
    return energy

def generate_random_boolean_function(n):
    truth_table = {}
    for i in range(2**n):
        truth_table[i] = random.choice([0, 1])
    return truth_table

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    clause = next(iter(cnf))
    for literal in clause:
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll(cnf - {clause}, new_assignment):
            return True
        new_assignment[literal] = False
        if dpll(cnf - {clause}, new_assignment):
            return True
    return False

def simulate_acc0_circuit(f, max_depth=4):
    cnf = []
    for a in range(2**n):
        for b in range(a, 2**n):
            for c in range(b, 2**n):
                d = (a + b - c) % (2**n)
                clause = [-(a+1), -(b+1), c+1, d+1]
                cnf.append(clause)
    return dpll(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 4
    f = generate_random_boolean_function(n)
    energy = truth_table_additive_energy(f)
    circuit_size = simulate_acc0_circuit(f)
    conjecture_holds = energy <= 2**(n/2) or circuit_size >= 2**(n/4)
    counterexample = "" if conjecture_holds else "energy={} < 2^{}/2 or circuit_size>=2^{}/4".format(energy, n, n)
    return {
        "metric_name": "Additive Energy",
        "metric_value": energy,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)

    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    std_energy = (sum((r["metric_value"] - mean_energy)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_energy, std_energy, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[seeds.index(first_failing_seed)]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")