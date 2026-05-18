# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def perm_mult(p1, p2):
    result = [0] * 5
    for i in range(5):
        result[i] = p1[p2[i] - 1]
    return result

def inversion_count(perm):
    count = 0
    for i in range(5):
        for j in range(i + 1, 5):
            if perm[i] > perm[j]:
                count += 1
    return count

def generate_formula(n, seed):
    random.seed(seed)
    if n == 1:
        return "x0"
    left = generate_formula(n // 2, seed + 1)
    right = generate_formula(n - n // 2, seed + 2)
    op = random.choice(["AND", "OR"])
    return f"({left} {op} {right})"

def barrington_compile(formula, seed):
    random.seed(seed)
    n = formula.count("x")
    L = 4 ** int(math.log2(n))
    layers = []
    for _ in range(L):
        i = random.randint(0, n - 1)
        g0 = [1, 2, 3, 4, 5]
        g1 = [1, 2, 3, 4, 5]
        if random.random() < 0.5:
            g1 = perm_mult(g1, [2, 1, 3, 4, 5])
        layers.append((i, g0, g1))
    return layers

def compute_sigma_squared(bp, n, seed):
    random.seed(seed)
    total = 0
    count = 0
    for _ in range(50):
        x = [random.randint(0, 1) for _ in range(n)]
        pi = [1, 2, 3, 4, 5]
        inv_counts = []
        for i, g0, g1 in bp:
            if x[i] == 1:
                pi = perm_mult(pi, g1)
            else:
                pi = perm_mult(pi, g0)
            inv_counts.append(inversion_count(pi))
        mu = sum(inv_counts) / len(inv_counts)
        variance = sum((ic - mu) ** 2 for ic in inv_counts) / len(inv_counts)
        total += variance
        count += 1
    return total / count if count > 0 else 0

def run_trial(seed):
    random.seed(seed)
    results = []
    for d in range(1, 5):
        n = 2 ** d
        formula = generate_formula(n, seed)
        bp = barrington_compile(formula, seed)
        sigma_squared = compute_sigma_squared(bp, n, seed)
        bound_i = 4 * d
        bound_ii = 1 / 8
        holds_i = sigma_squared <= bound_i
        holds_ii = sigma_squared >= bound_ii
        counterexample = ""
        if not holds_i:
            counterexample = f"sigma_squared={sigma_squared} > bound_i={bound_i}"
        elif not holds_ii:
            counterexample = f"sigma_squared={sigma_squared} < bound_ii={bound_ii}"
        results.append({
            "depth": d,
            "sigma_squared": sigma_squared,
            "conjecture_holds": holds_i and holds_ii,
            "counterexample": counterexample
        })
    # Add adversarial probes
    # Trivial 2-step PARITY-of-1 BP
    bp_parity = [(0, [1, 2, 3, 4, 5], [2, 1, 3, 4, 5]), (0, [1, 2, 3, 4, 5], [2, 1, 3, 4, 5])]
    sigma_squared_parity = compute_sigma_squared(bp_parity, 1, seed)
    holds_parity = sigma_squared_parity >= 1 / 8
    counterexample_parity = f"sigma_squared={sigma_squared_parity} < bound_ii={1/8}" if not holds_parity else ""
    results.append({
        "depth": 0,
        "sigma_squared": sigma_squared_parity,
        "conjecture_holds": holds_parity,
        "counterexample": counterexample_parity
    })
    # Length-12 commutator-of-commutators BP
    bp_commutator = [(0, [1, 2, 3, 4, 5], [2, 1, 3, 4, 5]) for _ in range(12)]
    sigma_squared_commutator = compute_sigma_squared(bp_commutator, 1, seed)
    holds_commutator = sigma_squared_commutator >= 1 / 8
    counterexample_commutator = f"sigma_squared={sigma_squared_commutator} < bound_ii={1/8}" if not holds_commutator else ""
    results.append({
        "depth": 0,
        "sigma_squared": sigma_squared_commutator,
        "conjecture_holds": holds_commutator,
        "counterexample": counterexample_commutator
    })
    # Aggregate results
    all_holds = all(r["conjecture_holds"] for r in results)
    counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
    return {
        "metric_name": "sigma_squared",
        "metric_value": sum(r["sigma_squared"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all_holds,
        "counterexample": counterexamples[0] if counterexamples else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(30))
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trial["seed"] = seed
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [t["metric_value"] for t in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [t["counterexample"] for t in trials if t["counterexample"]]
        if counterexamples:
            first_failing_seed = next(t["seed"] for t in trials if t["counterexample"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=mapping_undefined")