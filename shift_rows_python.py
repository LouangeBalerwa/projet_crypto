# L'étape Shift-Rows dans AES consiste à déplacer les lignes de la matrice d'état.
# En Python, vous pouvez implémenter l'étape Shift-Rows comme suit :

def shift_rows_AES(state):
   
    # Déplace la deuxième ligne d'une position vers la gauche
    state[1] = state[1][1:] + state[1][:1]
    
    # Déplace la troisième ligne de deux positions vers la gauche
    state[2] = state[2][2:] + state[2][:2]
    
    # Déplace la quatrième ligne de trois positions vers la gauche
    state[3] = state[3][3:] + state[3][:3]
    
    return state

# Exemple d'utilisation :
matrice_etat = [
    [0x32, 0x88, 0x31, 0xe0],
    [0x43, 0x5a, 0x31, 0x37],
    [0xf6, 0x30, 0x98, 0x07],
    [0xa8, 0x8d, 0xa2, 0x34]
]

# mat_apres_decalage = shift_rows_AES(matrice_etat)
# print(mat_apres_decalage)

    
original_row = [0x43, 0x5a, 0x31, 0x37]
shifted_row = original_row[3:] + original_row[:3]


print(f"Original row: {original_row}")
print(f"Shifted row: {shifted_row}")
