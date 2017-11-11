import re


def reformat(s):
    dict = ['of', 'the', 'with', '&']
    s = re.sub('([A-Z]{1})', r' \1', s)
    for i in range(len(dict)):
        s = s.replace(dict[i], " " + dict[i])
    s = s[1:]
    return s

s = "RisottowithPeas&Saffron"
print(reformat(s))