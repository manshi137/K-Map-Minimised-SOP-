from symbol import term
from tkinter import *
from PIL import Image, ImageTk
import numpy
# from K_map_gui_tk import *
def bintoexp(binarray):
    exparray = []
    for x in binarray:
        exp = ""
        for i in range(len(x)):
            if x[i]!="-":
                exp+= chr(i+97)
                if x[i]=='0':
                    exp+="'"
        exparray.append(exp)
    return exparray

def exptobin(exparray):
    term_array=[]
    for t in exparray: # ab in col,  cd in row
        tt = ""
        tt_arr =[]
        i=0
        while i<len(t):
            if i+1<len(t):
                if ord(t[i+1])<97: #apostrophe
                    # tt_arr.append(0)
                    tt = tt+"0"
                    i=i+2
                else:
                    # tt_arr.append(1)
                    tt = tt+"1"
                    i=i+1
            else:
                # tt_arr.append(1)
                tt = tt+"1" 
                i=i+1
        # print(tt)
        term_array.append(tt)
    # print(term_array)
    return term_array

def onebitdiff(one , two):
    ans = ""
    c=0
    for i in range(len(one)):
        if one[i]!= two[i]:
            ans+="-"
            c+=1
            if c>1:
                return(False, None)
        else:
            ans+=one[i]
    return (True, ans)

def removedc(terms, dc):
    ans = []
    for i in terms:
        if i not in dc:
            ans.append(i)
    return ans

def findexpterm(term, allterms):
    nones =  term.count('-')
    if nones ==0:
        if term in allterms:
            return [term]
        else:
            return []
    else:
        ind= term.find('-')
        ans = []
        if(ind!=-1):
            term1= term[:ind]+'1'+ term[ind+1:]
            term2= term[:ind]+'0'+ term[ind+1:]
            ans1 = findexpterm(term1, allterms)
            ans2 = findexpterm(term2, allterms)
            ans+=ans1
            ans+=ans2
        return ans

def bintovar(term):
    ans = []
    for i in range(len(term)):
        if term[i]=='0':
            ans.append(chr(i+97)+"'")
        elif term[i]=='1':
            ans.append(chr(i+97))
    return ans

def opt_function_reduce(func_TRUE, func_DC):
    trueterms = exptobin(func_TRUE)
    dcterms = exptobin(func_DC)
    n = len(trueterms[0])
    table = {}
    primeimp = set()
    allterms = trueterms + dcterms

    # making a dictionary with key = no. of ones, value = term
    for term in allterms:
        # print(f"term {term}{type(term)}")
        c=0
        for t in term:
            if t=='1':
                c+=1
        # print(c)
        # table[term.count("1")].append(term)
        if c in table.keys():
            table[c].append(term)
        else:
            table[c]=[term]
    print(f"table : {table}")

    # minimising terms
    while True:
        temptable = table.copy()
        visited=set()
        table = {}
        ind = 0
        listofkeys = list(temptable.keys())
        listofkeys.sort()
        for i in range(len(listofkeys)-1):
            for j in temptable[listofkeys[i]]:
                for k in temptable[listofkeys[i+1]]:
                    if(onebitdiff(j,k)[0]):
                        if ind in table.keys():
                            table[ind].append(onebitdiff(j,k)[1])
                        else:
                            table[ind] = [onebitdiff(j,k)[1]]
                        visited.add(j)
                        visited.add(k)
            ind +=1
        # temptable = numpy.flatten(temptable)
        # temptable = temptable.flatten()
        templist =[]
        for x in temptable.values():
            for xx in x:
                templist.append(xx)

        unvisited = set(templist).difference(visited)
        primeimp = primeimp.union(unvisited)
        
        if len(table) ==0:
            # print(f"table : {table}")
            print("Process of grouping terms completed")
            break

    matrix = {}
    if len(primeimp)>0:
        print(f"Terms whose max-legal-region cannot be expanded further : {primeimp}")
    for i in primeimp:
        expterm = findexpterm(i, allterms)
        expterm = removedc(expterm, dcterms)

        for j in expterm:
            if j in matrix.keys():
                matrix[j].append(i)
            else:
                matrix[j]=[i]

    essentialprimeimp = []
    for i in matrix.keys():
        if len(matrix[i])==1:
            if matrix[i][0] not in essentialprimeimp:
                essentialprimeimp.append(matrix[i][0])
                # for j in findexpterm(matrix[i][0]):
                #     del matrix[j]

    print(f"Essential Prime Implicants (terms which can not be contained in other max-legal-regions) : {essentialprimeimp}")
    # print(f"matrix................................")
    # print(f"{matrix}")
    matlist=[]
    for v in matrix.values():
        a=[]
        for j in v:
            a.append(bintovar(j))
        matlist.append(a)
    extra=[]
    for i in matlist:
        if i not in extra:
            extra.append(i)
    # print("...................................")
    # print(f"matlist {matlist}")
    # print("...................................")
    for i in essentialprimeimp:
        for j in findexpterm(i, allterms):
            if j in matrix.keys():
                del matrix[j]
    
    if len(matrix)==0:
        ans = bintoexp(essentialprimeimp)
        print("Max-legal regions are not completely contained in other regions")
        print("No regions can be deleted further")
        print(f"Final reduced minterms : {ans}")
        return ans
    else :
        # extra= []
        multterms = []
        for i in matrix.keys():
            multexp = []
            for j in matrix[i]:
                multexp.append(bintovar(j))
                # if(bintovar(j) not in extra ):
                #     extra.append(bintovar(j))
            multterms.append(multexp)
        # print(f"multterms before : {multterms}")
        dupl= multterms.copy()
        # # dupl+=
        # print(f" extra matrix {extra}")
        # print(f" duplicate of mutterms before {dupl}")
        while(len(multterms)>1):
            term1 = multterms[0]
            term2 = multterms[1]
            multterms.pop(0)
            # multterms[0]= multiply(term1, term2) start
            prod = []
            for t1 in term1:
                for t2 in term2:
                    p = []
                    for tt1 in t1:
                        if tt1+"'" in t2:
                            continue
                        elif len(tt1) ==2 and tt1[0] in t2:
                            continue
                        else:
                            p.append(tt1)
                    for tt2 in t2:
                        if tt2 not in p:
                            p.append(tt2)

                    if p not in prod:
                        prod.append(p)
            # multterms[0]= multiply(term1, term2) end
            multterms[0]= prod
        
        # print(f"multterms after : {multterms}")
        # print(f"appended term {min(multterms[0],key=len)}")
        richa = min(multterms[0],key=len)
        # print(f"-------{min(multterms[0],key=len)}")
        # l = len(multterms[0][0])
        # essentialprimeimp.append(multterms[0][0])
        # for m in multterms[0]:
        #     if len(m)< l:
        #         essentialprimeimp.pop()
        #         essentialprimeimp.append(m)
        #         print("mmmmm {m}")
        #         l = len(m)
        
                        

        # print(f"richa {richa}")
        # print(f"essential : {essentialprimeimp}")
        listextra=[]
        for v in essentialprimeimp:
            listextra.append(bintovar(v))
        listextra.append(richa)

        
        ans = bintoexp(essentialprimeimp)
        # print(f"Final reduced minterms : {ans}")
        ans.append(''.join(richa))

        red_dict = {}
        # print(f"listextra {listextra}")
        for i in extra:
            for m in i:
                reducedto=[]
                if m not in listextra:
                    for j in range(len(extra)):
                        if m in extra[j]:
                            # print(f"contained {i} in {dupl[j]}")
                            for k in extra[j]:

                                if k in listextra and (''.join(k) not in reducedto) :
                                    
                                    reducedto.append(''.join(k))  
                if ''.join(m) not in red_dict.keys():
                    red_dict[''.join(m)] = reducedto  
                # print(f"{m} is covered by {reducedto}")

        for k in red_dict.keys():
            if len(red_dict[k])>0:
                print(f"{k} is covered by {red_dict[k]}")
        print(f"Final reduced minterms : {ans}")
        return ans


# ----------------------------

# func_TRUE = ["abc'd'", "a'b'c'd", "a'bc'd", "ab'c'd", "a'bcd", "abcd", "ab'cd'"]
# func_DC= ["a'b'c'd'", "ab'c'd'", "abcd'"]

# func_TRUE = ["a'bcd", "a'bcd'", "abcd", "ab'cd"]
# func_DC = [ "abc'd", "ab'c'd"]
func_TRUE = ["a'b'c'd'", "ab'c'd'", "abc'd", "ab'c'd", "a'bcd" , "abcd" , "a'b'cd'", "ab'cd'"]
func_DC =  ["a'bcd'", "abcd'"]
opt_function_reduce(func_TRUE, func_DC)
