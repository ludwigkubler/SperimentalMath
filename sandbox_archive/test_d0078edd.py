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
from math import log2, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * log2(p) - (1 - p) * log2(1 - p)

    def self_dual_codes(clauses):
        n = len(clauses[0])
        codes = []
        for clause in clauses:
            code = [0] * n
            for literal in clause:
                if literal > 0:
                    code[literal - 1] = 1
                else:
                    code[-literal - 1] = -1
            codes.append(code)
        return codes

    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            clauses.append(clause)
        return clauses

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = int(2 ** (entropy(random.random()) * n))
            clauses = generate_sat_instance(n, m)
            codes = self_dual_codes(clauses)
            results.append({
                "n": n,
                "m": m,
                "codes": len(codes),
                "entropy": entropy(m / 2**n)
            })

    mean_n = sum(result["n"] for result in results) / len(results)
    std_dev = sqrt(sum((result["n"] - mean_n) ** 2 for result in results) / len(results))
    
    corr_coeff = sum((result["codes"] - mean_n) * (result["entropy"] - entropy(mean_n)) for result in results) / \
                 (sqrt(sum((result["codes"] - mean_n) ** 2 for result in results)) *
                  sqrt(sum((result["entropy"] - entropy(mean_n)) ** 2 for result in results)))

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(corr_coeff) >= 0.8 and all(abs(result["codes"] - mean_n) <= 3 * std_dev for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        trials.append(result)

    mean_corr_coeff = sum(trial["metric_value"] for trial in trials) / len(trials)
    std_dev_corr_coeff = sqrt(sum((trial["metric_value"] - mean_corr_coeff) ** 2 for trial in trials) / len(trials))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_dev_corr_coeff} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(seed for seed, trial in zip(seeds, trials) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")