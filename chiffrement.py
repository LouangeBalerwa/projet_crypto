import math as m

# chiffrement avec RSA
def rsa(texteplain,n,e):
    cipherText = []
    codeChart = "abcdefghijklmnopqrstuvwxyz123456789"
    tab_str = " "
    for key in codeChart:
        for i in texteplain:
            if key == i:
                char = codeChart.index(key)
                # print(char)
                c = int(m.pow(char,e)%n)
                # print(c)
                c = c%26
                char2  = codeChart[c]
                # print(c)
                cipherText.append(char2)
    # tab_str = ''.join(cipherText)
    for texte in cipherText:
        tab_str += texte
    # print(tab_str)
    return tab_str

# message ="h3i1230"
# print (rsa(message,33,3))       

