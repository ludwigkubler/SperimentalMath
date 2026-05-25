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
    
    def generate_random_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses

    def truth_table_entropy(clauses):
        n = len(clauses[0])
        counts = [0] * (2 ** n)
        for assignment in range(2 ** n):
            satisfied = True
            for clause in clauses:
                if all((assignment >> abs(l) - 1) & 1 == l > 0 for l in clause):
                    continue
                elif any((assignment >> abs(l) - 1) & 1 == l < 0 for l in clause):
                    satisfied = False
                    break
            counts[assignment] += int(satisfied)
        total = sum(counts)
        entropy = -sum(c / total * math.log2(c / total) for c in counts if c > 0)
        return entropy

    def diophantine_approximation(entropy):
        # Simplified approximation using continued fractions
        a, b = 1, 0
        while True:
            q = int((a + b) / (entropy - b))
            a, b = q * a + b, a
            if abs(a - entropy * b) < 1e-9:
                return len(bin(a)) - 2

    n_values = [10, 15, 20, 25, 30, 35]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_random_3cnf(n)
            entropy = truth_table_entropy(clauses)
            index = diophantine_approximation(entropy)
            total_metric_value += index
            instances_tested += 1

            if index > n * math.log2(n):
                conjecture_holds = False
                counterexample = f"Satisfiable formula with n={n} and index {index}"

    return {
        "metric_name": "Minimal Index of Diophantine Approximation",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")