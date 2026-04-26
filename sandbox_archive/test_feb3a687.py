import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(instance):
        # Simple DPLL algorithm implementation
        if not instance:
            return 0
        for literal in instance[0]:
            new_instance = [clause for clause in instance[1:] if literal not in clause and -literal not in clause]
            depth = dpll(new_instance)
            if depth is not None:
                return 1 + depth
        return None
    
    def incidence_matrix(n, m):
        mat = [[0] * n for _ in range(m)]
        for i in range(m):
            literals = random.sample(range(1, n+1), 3)
            for literal in literals:
                mat[i][abs(literal) - 1] = 1 if literal > 0 else -1
        return mat
    
    def max_eigenvalue(mat):
        n = len(mat)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        def matrix_mult(A, B):
            result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
            return result
        
        def matrix_add(A, B):
            return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
        
        def scalar_mult(s, mat):
            return [[s * x for x in row] for row in mat]
        
        def gaussian_elimination(mat):
            A = [row[:] for row in mat]
            n = len(A)
            for i in range(n):
                max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
                A[i], A[max_row] = A[max_row], A[i]
                factor = 1 / A[i][i]
                A[i] = scalar_mult(factor, A[i])
                for j in range(n):
                    if i != j:
                        factor = A[j][i]
                        A[j] = matrix_add(A[j], scalar_mult(-factor, A[i]))
            return A
        
        def eigenvalue(mat):
            n = len(mat)
            identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            max_iter = 1000
            epsilon = 1e-6
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x * x for x in v))
            for _ in range(max_iter):
                w = matrix_mult(mat, v)
                lambda_ = sum(w[i] * v[i] for i in range(n)) / sum(v[i] * v[i] for i in range(n))
                if abs(lambda_ - max_eigenvalue(identity)) < epsilon:
                    return lambda_
                v = w
            return None
        
        mat = gaussian_elimination(mat)
        return eigenvalue(mat)
    
    n_values = [5, 8, 11, 14]
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        m = random.randint(2 * n, 3 * n)
        instance = incidence_matrix(n, m)
        depth = dpll(instance)
        if depth is not None:
            total_depth += depth
            instances_tested += 1
    
    avg_depth = total_depth / instances_tested if instances_tested > 0 else 0
    max_lambda = max_eigenvalue(incidence_matrix(n, m))
    
    conjecture_holds = abs(avg_depth - max_lambda) < 0.1 * max_lambda
    counterexample = "" if conjecture_holds else f"avg_depth={avg_depth}, max_lambda={max_lambda}"
    
    return {
        "metric_name": "DPLL Depth vs Max Eigenvalue",
        "metric_value": avg_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        mean_depth = sum(r["metric_value"] for r in results) / len(results)
        std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")