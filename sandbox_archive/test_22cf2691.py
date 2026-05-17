# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def compute_kappa(supports, n):
    max_displacement = 0
    for S in supports:
        displacement_counts = defaultdict(int)
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                a, b = S[i], S[j]
                if a > b:
                    delta = a - b
                else:
                    delta = n - (b - a)
                displacement_counts[delta] += 1
        max_displacement = max(max_displacement, sum(displacement_counts.values()))
    return math.log2(1 + max_displacement)

def generate_minterm_dnf(n):
    supports = []
    for i in range(2 ** (n - 1)):
        S = []
        for j in range(n):
            if (i >> j) & 1:
                S.append(j)
        supports.append(S)
    return supports

def generate_random_dnf(n, size):
    supports = []
    for _ in range(size):
        S = random.sample(range(n), random.randint(1, n))
        supports.append(S)
    return supports

def generate_recursive_sigma3(n):
    if n == 1:
        return [[0]]
    sqrt_n = int(math.ceil(math.sqrt(n)))
    block_size = (n + sqrt_n - 1) // sqrt_n
    supports = []
    for i in range(sqrt_n):
        start = i * block_size
        end = min((i + 1) * block_size, n)
        block_supports = generate_recursive_sigma3(end - start)
        for S in block_supports:
            supports.append([x + start for x in S])
    return supports

def generate_majority_circuit(n):
    supports = []
    for i in range(n):
        S = [i]
        supports.append(S)
    return supports

def generate_and_circuit(n):
    supports = []
    for i in range(n):
        S = [i]
        supports.append(S)
    return supports

def generate_threshold_k_circuit(n, k):
    supports = []
    for i in range(k):
        S = [i]
        supports.append(S)
    return supports

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40]
    d_values = [2, 3]
    results = []
    instances_tested = 0

    for n in n_values:
        for d in d_values:
            threshold = (1/4) * (n ** (1/(d-1)))

            # Test minterm DNF
            supports = generate_minterm_dnf(n)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa >= threshold
            counterexample = "" if conjecture_holds else f"minterm_dnf n={n} d={d} kappa={kappa} < threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "minterm_dnf"
            })
            instances_tested += 1

            # Test recursive Σ3
            supports = generate_recursive_sigma3(n)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa >= threshold
            counterexample = "" if conjecture_holds else f"recursive_sigma3 n={n} d={d} kappa={kappa} < threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "recursive_sigma3"
            })
            instances_tested += 1

            # Test random DNF
            supports = generate_random_dnf(n, 2**n)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa < threshold
            counterexample = "" if conjecture_holds else f"random_dnf n={n} d={d} kappa={kappa} >= threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "random_dnf"
            })
            instances_tested += 1

            # Test majority circuit
            supports = generate_majority_circuit(n)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa < threshold
            counterexample = "" if conjecture_holds else f"majority_circuit n={n} d={d} kappa={kappa} >= threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "majority_circuit"
            })
            instances_tested += 1

            # Test AND circuit
            supports = generate_and_circuit(n)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa < threshold
            counterexample = "" if conjecture_holds else f"and_circuit n={n} d={d} kappa={kappa} >= threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "and_circuit"
            })
            instances_tested += 1

            # Test threshold-k circuit
            k = random.randint(1, n)
            supports = generate_threshold_k_circuit(n, k)
            kappa = compute_kappa(supports, n)
            conjecture_holds = kappa < threshold
            counterexample = "" if conjecture_holds else f"threshold_k_circuit n={n} d={d} kappa={kappa} >= threshold={threshold}"
            results.append({
                "metric_name": "kappa",
                "metric_value": kappa,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample,
                "seed": seed,
                "n": n,
                "d": d,
                "circuit_type": "threshold_k_circuit"
            })
            instances_tested += 1

    return {
        "metric_name": "kappa",
        "metric_value": sum(r["metric_value"] for r in results) / len(results),
        "instances_tested": instances_tested,
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": next((r["counterexample"] for r in results if not r["conjecture_holds"]), ""),
        "seed": seed
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")