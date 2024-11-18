import numpy as np

def calc_entropies(p_A=None, p_B_given_A=None, p_A_given_B=None, p_joint=None, p_B=None):
    if p_B_given_A is not None and p_A is not None:
        # Проверка на соответствие размеров
        if p_B_given_A.shape[0] != len(p_A):
            raise ValueError("Число строк в p(B|A) должно совпадать с количеством элементов в p(A).")
        
        # Вычисление p(B) через p(A) и p(B|A)
        p_B = np.sum(p_A[:, np.newaxis] * p_B_given_A, axis=0)
        p_joint = p_A[:, np.newaxis] * p_B_given_A

    elif p_A_given_B is not None and p_B is not None:
        # Проверка на соответствие размеров
        if p_A_given_B.shape[1] != len(p_B):
            raise ValueError("Число столбцов в p(A|B) должно совпадать с количеством элементов в p(B).")
        
        # Вычисление p(A) через p(A|B) и p(B)
        p_A = np.sum(p_A_given_B * p_B[np.newaxis, :], axis=1)
        p_joint = p_A_given_B * p_B[np.newaxis, :]

    elif p_joint is not None:
        # Вычисление p(A) и p(B) через p(A,B)
        p_A = np.sum(p_joint, axis=1)
        p_B = np.sum(p_joint, axis=0)

    else:
        raise ValueError("Необходимо задать хотя бы один набор данных (p_A, p_B_given_A, p_A_given_B или p_joint).")

    # Проверка на корректность нормировки
    if not np.isclose(np.sum(p_A), 1):
        raise ValueError("Сумма p(A) должна быть равна 1.")
    if not np.isclose(np.sum(p_B), 1):
        raise ValueError("Сумма p(B) должна быть равна 1.")

    # Вычисление энтропий
    H_A = -np.sum(p_A * np.log2(p_A + 1e-9))
    H_B = -np.sum(p_B * np.log2(p_B + 1e-9))
    H_AB = -np.sum(p_joint * np.log2(p_joint + 1e-9))
    H_B_given_A = H_AB - H_A
    H_A_given_B = H_AB - H_B
    I_AB = H_A - H_A_given_B

    return H_A, H_B, H_AB, H_A_given_B, H_B_given_A, I_AB, p_joint, p_A_given_B, p_B_given_A
