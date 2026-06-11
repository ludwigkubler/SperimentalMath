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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses

    def frobenius_schur_indicator(cnf):
        n = len(cnf[0])
        indicator = 0
        for clause in cnf:
            product = 1
            for literal in clause:
                if literal == -1:
                    product *= -1
                elif literal == 1:
                    product *= 1
            indicator += product
        return abs(indicator) / len(cnf)

    def boolean_circuit_entanglement_complexity(cnf):
        n = len(cnf[0])
        complexity = 0
        for clause in cnf:
            complexity += len(clause)
        return complexity

    def correlation_coefficient(values1, values2):
        n = len(values1)
        mean1 = sum(values1) / n
        mean2 = sum(values2) / n
        numerator = sum((values1[i] - mean1) * (values2[i] - mean2) for i in range(n))
        denominator = math.sqrt(sum((values1[i] - mean1)**2 for i in range(n))) * math.sqrt(sum((values2[i] - mean2)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0

    n_values = [5, 10, 15, 20, 30, 40]
    fsi_values = []
    ec_values = []

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            fsi = frobenius_schur_indicator(cnf)
            ec = boolean_circuit_entanglement_complexity(cnf)
            fsi_values.append(fsi)
            ec_values.append(ec)

    correlation = correlation_coefficient(fsi_values, ec_values)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(fsi_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.8,
        "counterexample": "" if correlation > 0.8 else "Correlation below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation below threshold' first_failing_seed={first_failing_seed}")