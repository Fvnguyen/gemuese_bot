import re
#Calculates the normalized Levenshtein distance of 2 strings
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    matrix = [list(range(l1 + 1))] * (l2 + 1)
    for zz in list(range(l2 + 1)):
      matrix[zz] = list(range(zz,zz + l1 + 1))
    for zz in list(range(0,l2)):
      for sz in list(range(0,l1)):
        if s1[sz] == s2[zz]:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
        else:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    distance = float(matrix[l2][l1])
    result = 1.0-distance/max(l1,l2)
    return result


#Untested matching function
def matching(text,master_list):
    result_list = [levenshtein(text, x) for x in master_list]
    result = max(result_list)
    return result