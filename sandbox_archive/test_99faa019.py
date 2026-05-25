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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def seifert_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] = -1
            M[v][u] = -1
        for i in range(n):
            M[i][i] = len([j for j in range(n) if (i, j) in edges or (j, i) in edges])
        return M
    
    def resolution_proof_length(edges, n):
        clauses = []
        for u, v in edges:
            clauses.append((u, v))
            clauses.append((-u, -v))
        for i in range(n):
            clauses.append((i,))
            clauses.append((-i,))
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph_edges = generate_graph(n)
        M = seifert_matrix(graph_edges, n)
        R = resolution_proof_length(graph_edges, n)
        
        if len(M) != n or any(len(row) != n for row in M):
            return {"metric_name": "Seifert Matrix", "metric_value": None, 
                    "instances_tested": 1, "conjecture_holds": False, 
                    "counterexample": "Invalid Seifert matrix dimensions"}
        
        if len(M) > 2**n:
            return {"metric_name": "Seifert Matrix", "metric_value": len(M), 
                    "instances_tested": 1, "conjecture_holds": False, 
                    "counterexample": "Number of Seifert matrices exceeds 2^n"}
        
        if R < n**2:
            return {"metric_name": "Resolution Proof Length", "metric_value": R, 
                    "instances_tested": 1, "conjecture_holds": False, 
                    "counterexample": "Resolution proof length less than n^2"}
        
        results.append({"n": n, "S(G)": len(M), "R(G)": R})
    
    return {"metric_name": "Seifert Matrix", "metric_value": sum(result["S(G)"] for result in results) / len(results),
            "instances_tested": len(results), "conjecture_holds": True, 
            "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No seeds supported the conjecture")