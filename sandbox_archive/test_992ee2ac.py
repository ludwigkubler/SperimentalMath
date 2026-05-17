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
    supports = []
    for i in range(1, 2**n):
        if bin(i).count('1') % 2 == 1:
            supports.append(set(j for j in range(n) if (i & (1 << j)) != 0))
    return supports

def generate_random_dnf(n, size):
    """Generate a random DNF with given size."""
    supports = []
    for _ in range(size):
        k = random.randint(1, n)
        support = set(random.sample(range(n), k))
        supports.append(support)
    return supports

def generate_block_parity_dnf(n, block_size):
    """Generate a Σ_3 PARITY circuit by partitioning [n] into blocks."""
    num_blocks = (n + block_size - 1) // block_size
    supports = []
    for i in range(num_blocks):
        start = i * block_size
        end = min(start + block_size, n)
        block = set(range(start, end))
        supports.append(block)
    return supports

def compute_kappa(supports, n):
    """Compute the Costas displacement defect κ(C)."""
    max_displacement = 0
    for S in supports:
        displacement_counts = defaultdict(int)
        for a, b in itertools.combinations(S, 2):
            if a > b:
                delta = a - b
                displacement_counts[delta] += 1
        if displacement_counts:
            max_displacement = max(max_displacement, max(displacement_counts.values()))
    return math.log2(1 + max_displacement)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40]
    d_values = [2, 3]
    total_parity_supported = 0
    total_non_parity_violated = 0
    total_instances = 0
    counterexample = ""

    for n in n_values:
        for d in d_values:
            # Generate PARITY circuits
            minterm_supports = generate_minterm_dnf(n)
            kappa_minterm = compute_kappa(minterm_supports, n)
            threshold = (1/4) * (n ** (1/(d-1)))
            if kappa_minterm < threshold:
                counterexample = f"minterm_dnf n={n} d={d} kappa={kappa_minterm} < threshold={threshold}"
                return {
                    "metric_name": "kappa",
                    "metric_value": kappa_minterm,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }

            block_size = int(math.sqrt(n))
            block_supports = generate_block_parity_dnf(n, block_size)
            kappa_block = compute_kappa(block_supports, n)
            if kappa_block < threshold:
                counterexample = f"block_parity_dnf n={n} d={d} kappa={kappa_block} < threshold={threshold}"
                return {
                    "metric_name": "kappa",
                    "metric_value": kappa_block,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }

            # Generate non-PARITY circuits
            for _ in range(5):
                random_supports = generate_random_dnf(n, 2**n)
                kappa_random = compute_kappa(random_supports, n)
                if kappa_random < threshold:
                    total_non_parity_violated += 1
                total_instances += 1

    if counterexample:
        return {
            "metric_name": "kappa",
            "metric_value": 0.0,
            "instances_tested": total_instances,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    return {
        "metric_name": "kappa",
        "metric_value": 1.0,
        "instances_tested": total_instances,
        "conjecture_holds": True,
        "counterexample": ""
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=11")