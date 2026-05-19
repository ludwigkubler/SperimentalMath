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
    
    def treewidth(G):
        if not G:
            return 0
        n = len(G)
        for u in range(n):
            neighbors = [v for v in range(n) if G[u][v]]
            if len(neighbors) == 1:
                continue
            for v in neighbors:
                G[v].remove(u)
                G[u].remove(v)
                tw = treewidth([G[i] for i in range(n) if i != u and i != v])
                G[v].append(u)
                G[u].append(v)
                if tw > 0:
                    return tw + 1
        return 0
    
    def tseitin_formula(G):
        n = len(G)
        literals = list(range(1, 2*n+1))
        clauses = []
        for u in range(n):
            if not G[u]:
                continue
            clause = [-literals[2*u], -literals[2*u+1]]
            clauses.append(clause)
            for v in G[u]:
                clause = [literals[2*v], literals[2*u+1]]
                clauses.append(clause)
        return clauses
    
    def resolution_length(clauses):
        if not clauses:
            return 0
        queue = list(clauses)
        while queue:
            c1 = queue.pop()
            for c2 in queue[:]:
                common_literals = [l for l in c1 if -l in c2]
                if not common_literals:
                    continue
                new_clause = [l for l in c1 + c2 if l not in common_literals and -l not in common_literals]
                if len(new_clause) == 0:
                    return float('inf')
                queue.append(new_clause)
        return len(queue)
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    tw = treewidth(G)
    formula = tseitin_formula(G)
    length = resolution_length(formula)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": n,
        "conjecture_holds": length >= 2**math.ceil(tw * math.log(2, 10)),
        "counterexample": "" if conjecture_holds else f"Treewidth={tw}, Length={length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")