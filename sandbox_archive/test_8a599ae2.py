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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    def dpll(cnf):
        if not cnf:
            return True
        literal = random.choice([x for clause in cnf for x in clause if abs(x) == 1])
        polarity = literal > 0
        literals = [x for clause in cnf for x in clause]
        new_cnf = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_clause = [x for x in clause if x != -literal]
                if new_clause:
                    new_cnf.append(new_clause)
            elif -literal in clause:
                return False
        return dpll(new_cnf) or dpll([[-x] for x in literals])

    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            cnf.append(clause)
        return cnf

    def quandle_operation(truth_table, x, y):
        result = [truth_table[x - 1][y - 1] for _ in range(len(truth_table))]
        return result

    def minimal_local_coherence_index(quandle):
        n = len(quandle)
        coherence_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                coherence_matrix[i][j] = sum(1 for x in range(1, n + 1) if quandle_operation(quandle, x, i + 1)[x - 1] != quandle_operation(quandle, x, j + 1)[x - 1])
        return sum(sum(row) for row in coherence_matrix) / (n * (n - 1))

    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            cnf = generate_random_cnf(n, n * (n - 1) // 2)
            if dpll(cnf):
                proof_length = len(cnf)
            else:
                proof_length = float('inf')
            quandle = [[i % n + 1 for i in range(1, n + 1)] for _ in range(n)]
            local_coherence_index = minimal_local_coherence_index(quandle)
            results.append({
                "metric_name": "LocalCoherenceIndex",
                "metric_value": local_coherence_index,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": abs(local_coherence_index - proof_length) <= 3,
                "counterexample": ""
            })

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = (sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(result["mean_metric"] for result in results) / len(results)
    std_metric = (sum((result["mean_metric"] - mean_metric) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")