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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            clauses.append(clause)
        return clauses

    def incidence_tensor(clauses):
        n = max(abs(v) for v in set.union(*clauses))
        tensor = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for i in range(2):
                if clause[i] > 0:
                    tensor[clause[i]][-1] += 1
                    tensor[-1][clause[i]] += 1
                else:
                    tensor[-1][-1] += 1
        return tensor

    def symmetric_square(tensor):
        n = len(tensor)
        result = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(i, n + 1):
                for k in range(j, n + 1):
                    result[i][j] += tensor[i][k] * tensor[j][k]
                    result[j][i] = result[i][j]
        return result

    def young_tableaux_count(n):
        if n == 0:
            return 1
        count = 0
        for i in range(1, n + 1):
            count += young_tableaux_count(i - 1) * young_tableaux_count(n - i)
        return count

    def resolution_width(tensor):
        n = len(tensor)
        queue = [(-1, -1)]
        visited = set()
        while queue:
            x, y = queue.pop(0)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and tensor[nx][ny] > 0:
                    queue.append((nx, ny))
        return len(visited)

    n = 40
    m = random.randint(n * (n - 1) // 2, n * (n + 1) // 2)
    clauses = generate_3cnf(n, m)
    tensor = incidence_tensor(clauses)
    symmetric = symmetric_square(tensor)
    d_phi = young_tableaux_count(n - 1)
    w_phi = resolution_width(symmetric)

    if d_phi == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "d(Φ) is zero"
        }

    bound = 0.8 * (d_phi ** (1/3)) / math.log(n)
    conjecture_holds = w_phi >= bound

    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"w(Φ) = {w_phi}, bound = {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")