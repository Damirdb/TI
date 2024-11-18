import numpy as np

def calc_entropies(p_A=None, p_B_given_A=None, p_A_given_B=None, p_joint=None, p_B=None):
    # Определяем, какой тип данных был введен и вычисляем недостающие вероятности
    if p_B_given_A is not None and p_A is not None:
        # Вариант 1: даны p(A) и p(B|A)
        p_A = np.array(p_A)  # Преобразуем p(A) в массив
        p_B_given_A = np.array(p_B_given_A)  # Преобразуем p(B|A) в массив
        
        # Проверяем размерности
        if p_A.shape[0] != p_B_given_A.shape[0]:
            raise ValueError("Число элементов в p(A) должно совпадать с числом строк в p(B|A)")
        
        # Вычисляем p(B) и p(A, B)
        p_B = np.sum(p_A[:, np.newaxis] * p_B_given_A, axis=0)  # Находим p(B)
        p_joint = p_A[:, np.newaxis] * p_B_given_A  # Находим p(A, B)

    elif p_A_given_B is not None and p_B is not None:
        # Вариант 2: даны p(B) и p(A|B)
        p_B = np.array(p_B)  # Преобразуем p(B) в массив
        p_A_given_B = np.array(p_A_given_B)  # Преобразуем p(A|B) в массив
        
        # Проверяем размерности
        if p_B.shape[0] != p_A_given_B.shape[1]:
            raise ValueError("Число элементов в p(B) должно совпадать с числом столбцов в p(A|B)")
        
        # Вычисляем p(A) и p(A, B)
        p_A = np.sum(p_A_given_B * p_B[np.newaxis, :], axis=1)  # Находим p(A)
        p_joint = p_A_given_B * p_B[np.newaxis, :]  # Находим p(A, B)

    elif p_joint is not None:
        # Вариант 3: даны p(A, B)
        p_joint = np.array(p_joint)  # Преобразуем p(A, B) в массив
        p_A = np.sum(p_joint, axis=1)  # Находим p(A)
        p_B = np.sum(p_joint, axis=0)  # Находим p(B)

    else:
        raise ValueError("Необходимо ввести данные хотя бы для одного из случаев: p(A) и p(B|A), p(B) и p(A|B), или p(A, B)")

    # Проверки для p(A) и p(B), чтобы гарантировать, что это корректные вероятности
    if not np.isclose(np.sum(p_A), 1):
        raise ValueError("Сумма вероятностей p(A) должна быть равна 1")
    if not np.isclose(np.sum(p_B), 1):
        raise ValueError("Сумма вероятностей p(B) должна быть равна 1")

    # Проверки для условных вероятностей, если они заданы
    if p_B_given_A is not None and not np.allclose(np.sum(p_B_given_A, axis=1), 1):
        raise ValueError("Сумма вероятностей для каждой строки p(B|A) должна быть равна 1")
    if p_A_given_B is not None and not np.allclose(np.sum(p_A_given_B, axis=0), 1):
        raise ValueError("Сумма вероятностей для каждого столбца p(A|B) должна быть равна 1")

    # Вычисляем условные вероятности p(B|A) и p(A|B), если они ещё не заданы
    p_B_given_A = p_joint / p_A[:, np.newaxis] if p_B_given_A is None else p_B_given_A
    p_A_given_B = p_joint / p_B[np.newaxis, :] if p_A_given_B is None else p_A_given_B

    # Энтропии H(A) и H(B)
    H_A = -np.sum(p_A * np.log2(p_A + 1e-12))  # Добавляем маленькое число, чтобы избежать log(0)
    H_B = -np.sum(p_B * np.log2(p_B + 1e-12))

    # Совместная энтропия H(A,B)
    H_AB = -np.sum(p_joint * np.log2(p_joint + 1e-12))

    # Условные энтропии H(B|A) и H(A|B)
    H_B_given_A = -np.sum(p_joint * np.log2(p_B_given_A + 1e-12))
    H_A_given_B = -np.sum(p_joint * np.log2(p_A_given_B + 1e-12))

    # Взаимная информация I(A,B)
    I_AB = H_A - H_A_given_B  # Также может быть вычислена как I_AB = H_B - H_B_given_A

    # Возвращаем все найденные значения
    return H_A, H_B, H_AB, H_A_given_B, H_B_given_A, I_AB, p_joint, p_A_given_B, p_B_given_A, p_A, p_B
