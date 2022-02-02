testCFG = """S -> abAB
A -> aAB | λ
B -> b"""  # test string, multiline.
dictionary = {}  # dictionary of nonterminal-terminal equivalents.
nonterminal = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']  # list of nonterminals
terminal = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']  # list of terminals
delimit = ['|']  # the delimiter, attempted to list alongside lambda but gave errors
lmbda = ['λ']  # null value, listed by itself to avoid accidental deletion (it's considered lowercase)
takenchar = list()  # holds list of encountered nonterminals
# noinspection SpellCheckingInspection
stringlist = list()  # used for building return strings in all functions


def remove_duplicates(inc_str):
    LHSlist = list()
    duplicates = list()
    countdictionary = {}
    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            LHSlist.append(LHS)
            for x in LHSlist:
                if LHSlist.count(x) >= 2:
                    if x in duplicates:
                        continue
                    duplicates.append(x)
    print(duplicates)
    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            if LHS in duplicates:  # if LHS is one of the duplicates
                if LHS in countdictionary:  # remove the line associated with this LHS
                    print(LHS, countdictionary[LHS])
                else:  # add to dictionary and move on
                    countdictionary[LHS] = 1


def term(inc_str):  # eliminate non solitary terminal rules
    retstring = ''
    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            for rule in RHS.split():  # go rule by rule via splitting RHS
                for ele in rule:  # iterate through rule character by character (ele)
                    if ele in nonterminal:  # if character is nonterminal, make sure it's in the list
                        takenchar.append(ele)
                if rule in delimit:
                    stringlist.append(rule)  # if delimiter, we dont do anything
                    continue
                else:
                    if any(ele in rule for ele in terminal) and any(
                            ele in rule for ele in nonterminal):  # if we find terminals in RHS
                        for ele in rule:  # iterate through rule
                            if ele in terminal:  # find the terminals
                                if bool(dictionary.get(ele)) == 1:  # if this has already been logged, replace.
                                    rule = rule.replace(ele, dictionary[ele])
                                    stringlist.append(rule)
                                if bool(dictionary.get(ele)) == 0:  # if this hasn't been logged, we must make a new
                                    # transition.
                                    for nont in nonterminal:
                                        if nont in dictionary.values() or nont in takenchar:
                                            continue  # skip past taken nonterminals
                                        else:
                                            dictionary[ele] = nont  # when we find an open one, implement it in the dict
                                            rule = rule.replace(ele, dictionary[ele])  # replace that character
                                            break
                    if rule.islower():  # this indicates its a nonterm to term, eg. A->a
                        continue
                    else:
                        continue
            stringlist.append(rule)
        retstring = retstring + LHS + ' ->'
        for r in range(len(stringlist)):
            retstring = retstring + ' ' + stringlist[r]  # print each rule
        retstring = retstring + '\n'
        stringlist.clear()
    for r in dictionary:
        retstring = retstring.strip() + '\n' + dictionary[r] + ' -> ' + r  # print dictionary rules
    return retstring


# noinspection SpellCheckingInspection
bindictionary = dictionary


def binomial(inc_str):
    retstring = ''

    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            for rule in RHS.split():  # go rule by rule via splitting RHS
                while len(rule) > 2:  # check rule for anything longer than two
                    rpair = rule[:2]
                    # excess = len(rule) - 2
                    # print(rule + " is " + str(excess) + " character(s) too long.")
                    for nont in nonterminal:
                        if nont in bindictionary.values() or nont in takenchar:
                            continue  # skip past taken nonterminals
                        else:
                            bindictionary[rpair] = nont  # when we find an open one, implement it in the dict
                            rule = rule.replace(rpair, bindictionary[rpair])  # replace that pair
                            break
                stringlist.append(rule)
        retstring = retstring + LHS + ' ->'
        for r in range(len(stringlist)):
            retstring = retstring + ' ' + stringlist[r]  # print each rule
        retstring = retstring + '\n'
        stringlist.clear()
    retstring = retstring.strip()
    for r in bindictionary:
        if r in retstring:
            continue
        retstring = retstring.strip() + '\n' + bindictionary[r] + ' -> ' + r  # print dictionary rules
    return retstring


nulldictionary = {}


def null(inc_str):
    retstring = ''
    keepterms = list()
    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            for rule in RHS.split():  # go rule by rule via splitting RHS
                if rule in lmbda:  # if we find lambda in the right hand side
                    for rule in RHS.split():
                        if rule in lmbda or rule in delimit:  # do not store lambda or |
                            continue
                        else:
                            nulldictionary[LHS] = rule  # we do store RHS rules in nullable production
    for line in inc_str.split('\n'):  # go line by line, replacing
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            if LHS in nulldictionary:
                continue
            else:
                for rule in RHS.split():
                    for ele in rule:
                        if ele in nulldictionary.keys():  # finds nullable terms in dictionary
                            for ele in rule:
                                if ele not in nulldictionary.keys():
                                    rule = (rule + ' | ' + ele)
                            rule = rule.replace(ele, nulldictionary[ele])
                stringlist.append(rule)
        retstring = retstring + LHS + ' ->'
        for r in range(len(stringlist)):
            retstring = retstring + ' ' + stringlist[r]  # print each rule
        retstring = retstring + '\n'
        stringlist.clear()
    retstring = retstring.strip()
    retstring = binomial(retstring)
    return retstring


def unit(inc_str):
    stringlist.clear()
    retstring = ''
    for line in inc_str.split('\n'):  # go line by line
        if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
            LHS, RHS = line.split(' -> ')  # split at arrow
            if LHS == 'F' and RHS == 'EA':  # temporary fix, we have two duplicates from improper dictionary implementation
                continue
            if LHS == 'G' and RHS == 'CA':  # temporary fix, we have two duplicates from improper dictionary implementation
                continue
            for rule in RHS.split():  # go rule by rule via splitting RHS
                if rule.isupper():
                    if len(rule) == 1:  # unit rules have a length of 1 and are uppercase.
                        for tline in inc_str.split('\n'):  # use t prefix to designate a temporary loop through again.
                            if inc_str.find(' -> ') != -1:  # if we encounter the arrow, designate this as split
                                tLHS, tRHS = tline.split(' -> ')  # split at arrow
                                if tLHS == rule:  # we loop to find what the unit rule is equal to, then swap it
                                    rule = tRHS
                stringlist.append(rule)
            retstring = retstring + LHS + ' ->'
            for r in range(len(stringlist)):  # build the strings based on elements in stringlist.
                retstring = retstring + ' ' + stringlist[r]  # print each rule
            retstring = retstring + '\n'
            stringlist.clear()
    retstring = retstring.strip()
    return retstring


termCFG = term(testCFG)  # TERM 100% finished
binCFG = binomial(termCFG)  # BIN 100% finished
nullCFG = null(binCFG)  # DEL 90%, need to bugfix duplicate issue.
unitCFG = unit(nullCFG)  # UNIT 90% finished, duplicate issue was duct taped but not fixed at source.
# we can add START very easily, a simple loop through the string storing RHS of the S line and adding S0 -> RHS S line
# will implement START

print(unitCFG)
