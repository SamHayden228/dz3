import xml.etree.ElementTree as ET
import re

# Regex pattern splits on substrings "; " and ", "
parser =ET.XMLParser(encoding="utf-8")

class specs():
    def __init__(self,type,val):
        self.type=type
        self.val=val

def Operation(p):
    if p[1] == "[" and p[-1] == "]":
        s = p[2:-1].split(" ")
        stack = []

        for i in s:
            if i.isdigit():
                stack.append(int(i))
            elif re.match("[A-Z]+\[\s*([A-Z]+|\d+)\s*\]", i):
                k=i.replace("][","[").replace("]","").split("[")
                l=vars[k[0]].val
                for i in k[1:]:
                    if i.isdigit():
                        l=l[int(i)]
                    else:
                        l=l[i]
                if str(type(l)).count("int"):
                    stack.append(l)
                else:
                    print("Invalid operation notation")
                    print(f"{l} in {i} is not int")
                    return False

            elif re.match("[A-Z]+", i):
                if ((list(vars.keys()).count(i) and vars[i].type.count("int"))):
                    stack.append(i)
                else:
                    print("Invalid operation notation")
                    print(f"{i} either not defined or not int")
                    return False
            elif i=="+":
                stack.append(stack[-2]+stack[-1])
                stack.pop(-2)
                stack.pop(-2)
            elif i=="-":
                stack.append(stack[-2]-stack[-1])
                stack.pop(-2)
                stack.pop(-2)
            elif i=="^":
                stack.append(stack[-2]**stack[-1])
                stack.pop(-2)
                stack.pop(-2)
    if len(stack)==1:
        return stack[0]
    else:
        print(f"Something went wrong during calculation of {p}")
        return False

def Meaning(s):
    if s[0] == "#":

        h = s[2:-1]
        res=re.findall("#.*?[)]|[^\s]+",h)

        for i in range (len(res)):
            res[i]=Meaning(res[i])

        if res.count(False)!=0:
            return False
        return res
    elif s[0] == "{":
        h=s[1:-1].split(',')
        r={}
        for i in h:
            k=i.split(":")
            if re.match("[A-Z]+",k[0]):
                if (m:=Meaning(k[1])):
                    r[k[0]]=m
                else:
                    print("Invalid name notation")
                    return False

            else:
                return False
        return r
    elif s[0]=="S":
        return strings[s]
    elif s[0]=="?":
        return Operation(s)
    else:
        if s.isdigit():
            return int(s)
        print ("Invalid integer notation")
        return False


def Parce(program):

    for p in program:
        if p[:3] == "def":

            if (re.match(" [A-Z]+=", p[3:p.index("=") + 1])):

                if ( (list(vars.keys()).count(p[4:p.index("=")]))):
                    return ("Variable is already defined")

                mean = Meaning(p[p.index("=") + 1:])

                if mean:
                    vars[p[4:p.index("=")]] = specs(str(type(mean)), mean)
                else:
                    return False
            else:
                return ("Invalid initialization notation")

        else:
            if (not (p) or re.search("[A-Z]+=", p[:p.index("=") + 1])):
                if (not (list(vars.keys()).count(p[:p.index("=")]))):

                    return("Variable is not defined")

                mean = Meaning(p[p.index("=") + 1:])
                if mean:
                    if vars[p[:p.index("=")]].type != str(type(mean)):
                        return ("Type redefinition is not allowed")

                    vars[p[:p.index("=")]].val = mean
                else:
                    return False
            else:
                return ("Invalid notation")

    return vars


tree = ET.parse('C:/Users/vlaso_n8/PycharmProjects/pythonProject/konfig/dz3/konfig.xml',parser=parser)
root = tree.getroot()
rt=str(root.findall("program")[0].text).replace("\n","ß")
vars={}
strings={}
def main():
    program=(str(re.sub('[ß]+[" "]+', '', rt)))

    strs=re.findall('@"[^"]+"',program)

    for i in range(len(strs)):
        program=program.replace(strs[i],f"S{i}")
        strings[f"S{i}"]=strs[i][2:-1]
    program=program.split(";")


    vars=Parce(program)

    if not(str(type(vars)).count("dict")):
        return vars
    res=""
    for i in vars.keys():
        res+=f"{i}, type {vars[i].type}, val {vars[i].val}\n"

    return (res)


if __name__ == "__main__":
    print(main())



