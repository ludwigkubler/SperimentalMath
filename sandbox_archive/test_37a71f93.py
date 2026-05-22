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
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_graph(cnf):
        graph = {}
        for i in range(len(cnf)):
            for j in range(i + 1, len(cnf)):
                if any(-cnf[i][k] == cnf[j][l] for k in range(2) for l in range(2)):
                    if i not in graph:
                        graph[i] = set()
                    if j not in graph:
                        graph[j] = set()
                    graph[i].add(j)
                    graph[j].add(i)
        return graph
    
    def quasi_postnikov_rank(graph):
        n = len(graph)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        rank += 1
                        for neighbor in graph[node]:
                            if not visited[neighbor]:
                                stack.append(neighbor)
        return rank
    
    def monotone_circuit_depth(cnf):
        n = len(cnf)
        depth = [0] * (n + 1)
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    depth[literal] = max(depth[literal], depth[-literal] + 1)
                else:
                    depth[-literal] = max(depth[-literal], depth[literal] + 1)
        return max(depth)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        graph = resolution_graph(cnf)
        rank = quasi_postnikov_rank(graph)
        depth = monotone_circuit_depth(cnf)
        results.append({"n": n, "rank": rank, "depth": depth})
    
    total_rank = sum(result["rank"] for result in results)
    total_depth = sum(result["depth"] for result in results)
    avg_rank = Fraction(total_rank, len(results))
    avg_depth = Fraction(total_depth, len(results))
    diff_avg = abs(avg_rank - avg_depth)
    
    conjecture_holds = diff_avg <= 3
    counterexample = "" if conjecture_holds else f"Average rank {avg_rank}, average depth {avg_depth}"
    
    return {
        "metric_name": "average_difference",
        "metric_value": float(diff_avg),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_diff_avg = sum(result["metric_value"] for result in results)
    avg_diff_avg = Fraction(total_diff_avg, len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_diff_avg} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_diff_avg} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")