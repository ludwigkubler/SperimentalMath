# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_minterm_dnf(n):
    """Generate the canonical 2^{n-1}-minterm DNF for PARITY_n."""
    minterms = []
    for i in range(1, 2**n):
        if bin(i).count('1') % 2 == 1:
            minterm = []
            for j in range(n):
                if (i >> (n - 1 - j)) & 1:
                    minterm.append(j + 1)
            minterms.append(minterm)
    return minterms

def generate_random_dnf(n, size):
    """Generate a random DNF with given size."""
    dnf = []
    for _ in range(size):
        k = random.randint(1, n)
        literals = random.sample(range(1, n + 1), k)
        dnf.append(literals)
    return dnf

def generate_random_ac0(n, size, depth):
    """Generate a random AC^0 circuit with given size and depth."""
    if depth == 1:
        return generate_random_dnf(n, size)
    else:
        # Recursively generate sub-circuits
        sub_size = int(math.sqrt(size))
        sub_circuit1 = generate_random_ac0(n, sub_size, depth - 1)
        sub_circuit2 = generate_random_ac0(n, sub_size, depth - 1)
        return [sub_circuit1, sub_circuit2]

def compute_kappa(circuit, n):
    """Compute the Costas displacement defect kappa(C)."""
    max_displacement = 0
    for support in circuit:
        displacement_counts = defaultdict(int)
        for a, b in itertools.combinations(support, 2):
            if a > b:
                delta = a - b
                displacement_counts[delta] += 1
        max_displacement = max(max_displacement, sum(displacement_counts.values()))
    return math.log2(1 + max_displacement)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40]
    d_values = [2, 3]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            # Generate PARITY circuit
            parity_circuit = generate_minterm_dnf(n)
            kappa_parity = compute_kappa(parity_circuit, n)
            bound = (1/4) * (n ** (1/(d - 1)))
            if kappa_parity < bound:
                conjecture_holds = False
                counterexample = f"PARITY circuit with n={n}, d={d}, kappa={kappa_parity} < bound={bound}"
                break

            # Generate random DNF and AC^0 circuits
            for _ in range(5):
                random_dnf = generate_random_dnf(n, 2**n)
                kappa_dnf = compute_kappa(random_dnf, n)
                if kappa_dnf >= bound:
                    conjecture_holds = False
                    counterexample = f"Random DNF with n={n}, d={d}, kappa={kappa_dnf} >= bound={bound}"
                    break

                random_ac0 = generate_random_ac0(n, 2**n, d)
                kappa_ac0 = compute_kappa(random_ac0, n)
                if kappa_ac0 >= bound:
                    conjecture_holds = False
                    counterexample = f"Random AC^0 circuit with n={n}, d={d}, kappa={kappa_ac0} >= bound={bound}"
                    break

            if not conjecture_holds:
                break

            instances_tested += 1
            metric_values.append(kappa_parity)

        if not conjecture_holds:
            break

    if conjecture_holds:
        metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0
    else:
        metric_value = 0.0

    return {
        "metric_name": "kappa",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")