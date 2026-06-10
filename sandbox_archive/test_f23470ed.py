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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def kneser_graph(cnf):
        V = set()
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    V.add((clause[i], clause[j]))
        E = []
        for v1 in V:
            for v2 in V:
                if v1 != v2 and len(set(v1) & set(v2)) == 1:
                    E.append((v1, v2))
        return V, E
    
    def automorphism_group(V, E):
        n = len(V)
        G = [[] for _ in range(n)]
        for u, v in E:
            i, j = V.index(u), V.index(v)
            G[i].append(j)
            G[j].append(i)
        
        def dfs(node, visited, perm):
            if node in visited:
                return True
            visited.add(node)
            perm[node] = len(visited) - 1
            for neighbor in G[node]:
                if not dfs(neighbor, visited, perm):
                    return False
            return True
        
        def is_isomorphic(G1, G2):
            n1, n2 = len(G1), len(G2)
            if n1 != n2:
                return False
            for p in itertools.permutations(range(n1)):
                H2 = [[] for _ in range(n2)]
                for u in range(n1):
                    for v in G1[u]:
                        H2[p[u]].append(p[v])
                if H2 == G2:
                    return True
            return False
        
        visited = set()
        perm = [-1] * n
        automorphisms = []
        for p in itertools.permutations(range(n)):
            H = [[] for _ in range(n)]
            for u in range(n):
                for v in G[u]:
                    H[p[u]].append(p[v])
            if is_isomorphic(H, G):
                automorphisms.append(p)
        return len(automorphisms)
    
    def min_degree(G):
        n = len(G)
        degrees = [0] * n
        for u in range(n):
            for v in G[u]:
                degrees[u] += 1
                degrees[v] += 1
        return max(degrees)
    
    def count_satisfying_assignments(cnf):
        n = len(cnf)
        satisfying_count = 0
        for i in range(2 ** n):
            assignment = [(i >> j) & 1 for j in range(n)]
            if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in cnf):
                satisfying_count += 1
        return satisfying_count
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    V, E = kneser_graph(cnf)
    perm_count = automorphism_group(V, E)
    min_deg = min_degree(E)
    sat_count = count_satisfying_assignments(cnf)
    
    return {
        "metric_name": "Automorphism Group Count and Minimum Degree",
        "metric_value": perm_count * min_deg,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": perm_count <= n**2 * math.log(n) and min_deg >= 2**n - sat_count,
        "counterexample": "" if perm_count <= n**2 * math.log(n) and min_deg >= 2**n - sat_count else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")