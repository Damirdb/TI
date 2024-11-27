import numpy as np

def shannon_entropy(prob_dist):
    # Вычисляет энтропию Шеннона для заданного распределения вероятностей.
    return -np.sum(prob_dist * np.log2(prob_dist, where=(prob_dist > 0)))

def conditional_entropy(p_cond, p_source):
    # Функция для расчета условной энтропии H(A|B) или H(B|A)
    if p_cond.shape[1] != p_source.shape[0]:
        p_source = p_source[:, np.newaxis]  
    joint_prob = p_cond * p_source  # Совместные вероятности P(AB)
    cond_entropy = -np.nansum(joint_prob * np.log2(p_cond), axis=0)
    return np.sum(cond_entropy)

def joint_entropy(p_joint):
    # Расчет совместной энтропии H(A, B)
    return -np.nansum(p_joint * np.log2(p_joint))

def mutual_information(H_A, H_B, H_AB):
    # Расчет взаимной информации I(A; B)
    return H_A + H_B - H_AB

def reverse_channel(p_joint, p_B):
    # Вычисляет обратную канальную матрицу p(ai|bj).
    return p_joint.T / p_B[:, np.newaxis]

# Вариант 1: ансамбль A и канальная матрица p(bj|ai)
def variant_1(p_b_given_a, p_A):
    p_joint = p_b_given_a * p_A[:, np.newaxis]
    p_B = np.sum(p_joint, axis=0)
    p_a_given_b = np.divide(p_joint, p_B, where=(p_B > 0))

    H_A = shannon_entropy(p_A)
    H_B = shannon_entropy(p_B)
    H_B_given_A = conditional_entropy(p_b_given_a, p_A)
    H_A_given_B = conditional_entropy(p_a_given_b.T, p_B)

    H_AB = joint_entropy(p_joint)
    I_AB = mutual_information(H_A, H_B, H_AB)

    if len(p_a_given_b.shape) == 2 and p_a_given_b.size == 8:  
        p_a_given_b = p_a_given_b.reshape(2, 4)

    return (
        np.round(p_A, 4),
        np.round(p_B, 4),
        np.round(H_A, 4),
        np.round(H_B, 4),
        np.round(H_A_given_B, 4),
        np.round(H_B_given_A, 4),
        np.round(H_AB, 4),
        np.round(I_AB, 4),
        np.round(p_a_given_b, 4),  
        np.round(p_b_given_a, 4),
        np.round(p_joint, 4)
    )

# Вариант 2: ансамбль B и канальная матрица p(ai|bj)
def variant_2(p_a_given_b, p_B):
    p_joint = p_a_given_b * p_B  
    p_A = np.sum(p_joint, axis=1)  
    p_b_given_a = reverse_channel(p_joint.T, p_A) 
    
    H_A = shannon_entropy(p_A)
    H_B = shannon_entropy(p_B)
    H_A_given_B = conditional_entropy(p_a_given_b.T, p_B)
    H_B_given_A = conditional_entropy(p_b_given_a, p_A)
    
    H_AB = joint_entropy(p_joint)
    I_AB = mutual_information(H_A, H_B, H_AB)
    
    return (
        np.round(p_A, 4),
        np.round(p_B, 4),
        np.round(H_A, 4),
        np.round(H_B, 4),
        np.round(H_A_given_B, 4),
        np.round(H_B_given_A, 4),
        np.round(H_AB, 4),
        np.round(I_AB, 4),
        np.round(p_a_given_b, 4),
        np.round(p_b_given_a, 4),
        np.round(p_joint, 4)
    )

# Вариант 3: Матрица p(aibj)
def variant_3(p_joint):
    p_A = np.sum(p_joint, axis=1)
    p_B = np.sum(p_joint, axis=0)

    H_A = shannon_entropy(p_A)
    H_B = shannon_entropy(p_B)
    H_AB = joint_entropy(p_joint)
    
    p_a_given_b = np.divide(p_joint, p_B, where=(p_B > 0))
    H_A_given_B = -np.nansum(p_joint * np.log2(p_a_given_b), axis=0).sum()
    
    p_b_given_a = np.divide(p_joint.T, p_A, where=(p_A > 0)).T
    H_B_given_A = -np.nansum(p_joint * np.log2(p_b_given_a), axis=1).sum()
    
    I_AB = mutual_information(H_A, H_B, H_AB)

    return (
        np.round(p_A, 4),
        np.round(p_B, 4),
        np.round(H_A, 4),
        np.round(H_B, 4),
        np.round(H_A_given_B, 4),
        np.round(H_B_given_A, 4),
        np.round(H_AB, 4),
        np.round(I_AB, 4),
        np.round(p_a_given_b, 4),
        np.round(p_b_given_a, 4),
        np.round(p_joint, 4)
    )