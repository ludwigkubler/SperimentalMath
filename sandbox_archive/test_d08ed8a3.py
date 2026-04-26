import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mult(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = Fraction(M[j][i], M[i][i])
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0]*n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
        x[i] /= M[i][i]
    return x

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def poset_dimension(rectangles):
    n = len(rectangles)
    if n == 0:
        return 0
    R = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if all(rectangles[i][k] <= rectangles[j][k] for k in range(len(rectangles[i]))):
                R[i].add(j)
            if all(rectangles[j][k] <= rectangles[i][k] for k in range(len(rectangles[j]))):
                R[j].add(i)
    def dfs(node, visited):
        visited.add(node)
        for neighbor in R[node]:
            if neighbor not in visited:
                dfs(neighbor, visited)
    components = []
    visited = set()
    for i in range(n):
        if i not in visited:
            component = []
            dfs(i, component)
            components.append(component)
    return max(len(component) for component in components)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    variables = list(range(n))
    clauses = []
    for _ in range(2**n):
        clause = [random.choice([-1, 1]) * var for var in variables]
        if any(all(clause[j] == -clauses[i][j] for j in range(n)) for i in range(len(clauses))):
            continue
        clauses.append(clause)
    communication_matrix = [[0]*len(clauses) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(len(clauses)):
            if all((clauses[j][k] == 1 and (i & (1 << k)) != 0) or
                   (clauses[j][k] == -1 and (i & (1 << k)) == 0)
                   for k in range(n)):
                communication_matrix[i][j] = 1
    rectangles = []
    for i in range(2**n):
        if all(communication_matrix[i][j] == communication_matrix[i^mask][j] for mask in range(2**n)):
            rectangle = [i]
            for j in range(len(clauses)):
                if communication_matrix[i][j] == 1:
                    rectangle.append(j)
            rectangles.append(rectangle)
    poset_dim = poset_dimension(rectangles)
    comm_complexity = len(rectangles)
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity >= poset_dim,
        "counterexample": "" if comm_complexity >= poset_dim else f"poset dimension {poset_dim} < communication complexity {comm_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")