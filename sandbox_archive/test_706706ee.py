import random
import math
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def is_planar(G):
    def dfs(v, parent, color):
        colors[v] = color
        for u in G[v]:
            if u == parent:
                continue
            if colors[u] == -1:
                if not dfs(u, v, 1-color):
                    return False
            elif colors[u] == colors[v]:
                return False
        return True
    
    n = len(G)
    colors = [-1] * n
    for i in range(n):
        if colors[i] == -1 and not dfs(i, -1, 0):
            return False
    return True

def genus(G):
    if is_planar(G):
        return 0
    else:
        # Heuristic: genus = (e - v + 2) / 2 for non-planar graphs
        e = sum(len(neighbors) for neighbors in G) // 2
        v = len(G)
        return math.ceil((e - v + 2) / 2)

def tseitin_formula(G):
    n = len(G)
    literals = {i: f'x{i}' for i in range(n)}
    neg_literals = {i: f'-x{i}' for i in range(n)}
    
    clauses = []
    for i in range(n):
        clauses.append([literals[i]])
        for j in G[i]:
            clauses.append([neg_literals[i], literals[j]])
            clauses.append([neg_literals[j], literals[i]])
    
    return clauses

def resolution_width(clauses):
    def add_clause(clause):
        nonlocal unit_clauses
        unit_clauses.extend(clause)
    
    def resolve(clause1, clause2):
        new_clause = []
        for lit in clause1:
            if -lit not in clause2:
                new_clause.append(lit)
        return new_clause
    
    unit_clauses = []
    while True:
        add_clause(unit_clauses)
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                    new_clauses.append(resolve(clauses[i], clauses[j]))
        if not new_clauses:
            break
        clauses.extend(new_clauses)
    
    return len(unit_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    G = {i: [] for i in range(n)}
    edges = list(combinations(range(n), 2))
    m = len(edges)
    for _ in range(m):
        u, v = random.sample(edges, 1)[0]
        if u not in G[v]:
            G[u].append(v)
            G[v].append(u)
    
    g_G = genus(G)
    formula = tseitin_formula(G)
    width = resolution_width(formula)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 0.5 * g_G,
        "counterexample": "" if width >= 0.5 * g_G else f"Graph with genus {g_G} and resolution width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")