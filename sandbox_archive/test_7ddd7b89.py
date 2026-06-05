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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_circuit(n, d):
        if n % d != 0:
            return None
        circuit = [[random.randint(0, 1) for _ in range(d)] for _ in range(n)]
        return circuit
    
    def compute_tropical_rank(circuit):
        n = len(circuit)
        m = len(circuit[0])
        rank = 0
        for i in range(m):
            row_sums = [sum(row[i] for row in circuit) for row in circuit]
            if any(x > 0 for x in row_sums):
                rank += 1
        return rank
    
    def compute_monotone_width(circuit):
        n = len(circuit)
        m = len(circuit[0])
        width = 0
        for i in range(m):
            max_sum = 0
            current_sum = 0
            for j in range(n):
                if circuit[j][i] == 1:
                    current_sum += 1
                else:
                    max_sum = max(max_sum, current_sum)
                    current_sum = 0
            max_sum = max(max_sum, current_sum)
            width = max(width, max_sum)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, min(n - 1, 2))
            circuit = generate_d_regular_circuit(n, d)
            if circuit is None:
                continue
            instances_tested += 1
            tropical_rank = compute_tropical_rank(circuit)
            monotone_width = compute_monotone_width(circuit)
            expected_bound = math.sqrt(d) * n ** (1/3)
            if abs(tropical_rank - monotone_width) > 0.5 * expected_bound:
                conjecture_holds = False
                counterexample = f"n={n}, d={d}, tropical_rank={tropical_rank}, monotone_width={monotone_width}"
    
    return {
        "metric_name": "Monotone Width",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std={std_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(abs(r["metric_value"] - r["expected_bound"]) > 0.5 * r["expected_bound"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")