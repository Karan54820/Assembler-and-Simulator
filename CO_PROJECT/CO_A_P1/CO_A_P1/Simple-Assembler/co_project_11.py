import sys
import re
import  struct 
# f=open("test.txt",'r')
# f2=open("test_result.txt",'w')
input_list=[]
answer=[]
variables=[]
var_value=[]

labels=[]
labels_val=[]
opcode={'add':'00000','sub':'00001','mov1':'00010','mov2':'00011','ld':'00100','st':'00101',
        'mul':'00110','div':'00111','rs':'01000','ls':'01001','xor':'01010','or':'01011',
        'and':'01100','not':'01101','cmp':'01110','jmp':'01111','jlt':'11100','jgt':'11101',
        'je':'11111','hlt':'11010','addf':'10000','subf':'10001','movf':'10010'}
register={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}
register1={'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0}
flags = {'V': 0, 'L': 0, 'G': 0, 'E': 0}
stmtypes = {"add": "A", "sub": "A","addf": "A","subf": "A", "mov1": "B", "mov2": "C", "ld": "D", "st": "D", 
            "mul": "A", "div": "C", "rs": "B","ls": "B", "xor": "A", "or": "A",
             "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E",
             "je": "E", "hlt": "F",'movf':"B"}

s=sys.stdin.read()
L=s.split("\n")
for line in L:
    line =line.strip()
    if not  line:
        continue #remove whit e
    splt=[splt.strip() for splt in line.split()]
    input_list.append(splt)# splititng into variable ....


def var_error(list):
    var_error=0
    if input_list[0][0]=='var':
        for i in range(1,len(input_list)):
            if input_list[i][0]=='var':
                if input_list[i-1][0]!='var':
                    var_error=1
                    return var_error
    else:
        var_error=1
        return var_error
#print(input_list)

for i in input_list:
    # print(i)
    if i[0][-1]==':':
        labels.append(i[0][:-1])
        
    if i[0]=='mov':
        if (i[2][0]=='$'):
            register1[i[1]]=int(i[2][1:])
            answer.append(opcode['mov1'])
            i[0]="mov1"

        else:
            answer.append(opcode['mov2'])
            i[0]="mov2"
    
    if i[0] in opcode:
        answer.append(opcode[i[0]])
    if i[0]=='var':
        variables.append(i[1])
        counter=0
        bincounter=bin(counter)[2:]# removing 0b and bin for conversion 
        
    if (i[-1])[-1]==':':
        labels.append(i[0][:-1])
        # print(labels)
    if i[0][-1]==":":
        counter=0
        bincounter=bin(counter)[2:]# removing 0b and bin for conversion 
        # print(bincounter)
        labels_val.append("{0:07b}".format(input_list.index(i)-len(variables)))
            # print(labels_val)
       
#     #CHECKING FOR OVERFLOW IN ADD    
    if i[0]=='add' and len(i)==4:
        register1[i[1]]=register1[i[2]]+register1[i[3]]
        if len(bin(register1[i[1]])[2:])>len(bin(register1[i[2]])[2:]) or len(bin(register1[i[1]])[2:]) > len (bin(register1[i[3]])[2:]):
            flags['V']=1
            register1[i[1]]=0
    
    # if i[0]=='addf' and len(i)==4:


    #CHECKING FOR OVERFLOW IN SUBTRACT
    elif i[0]=='sub' and len(i)==4:
        register1[i[1]]=register1[i[2]]-register1[i[3]]
        if bin(register1[i[2]])[2:]<bin(register1[i[3]])[2:]:
            flags['V']=1
            register1[i[1]]=0

#CHECKING FOR OVERFLOW IN MULTIPLY
    elif i[0]=='mul' and len(i)==4:
        register1[i[1]]=register1[i[2]]-register1[i[3]]
        if len(bin(register1[i[1]])[2:])>len(bin(register1[i[2]])[2:]) or len(bin(register1[i[1]])[2:]) > len (bin(register1[i[3]])[2:]):
            flags['V']=1
            register1[i[1]]=0

#CHECKING FOR OVERFLOW IN DIVISION
    elif i[0]=='div' and len(i)==3:
        if register1[i[2]]==0:
            register1['R0']=0
        else:
            register1['R0']=int(register1[i[1]]/register1[i[2]])
            register1["R1"]=register1[i[1]]%register1[i[2]]
            if register1[i[2]]==0:
                flags['V']=1
                register1["R0"]=0
                register1["R1"]=0

#   CHECKING FOR COMPARE FUNCTION     
    elif i[0]=='cmp' and len(i)==3:
        if register1[i[1]]<register1[i[2]]:
            flags['L']=1

        elif register1[i[1]]>register1[i[2]]:
            flags['G']=1

        elif register1[i[1]]<register1[i[2]]:
            flags['E']=1
copy_list=input_list.copy()
for i in input_list:
    if i[0][:-1] in labels:
        i.remove(i[0])

for i in range(len(variables)):
    var_value.append("{0:07b}".format(len(input_list)+i-len(variables)))

# print(variables)
# print(len(input_list))
#print(input_list)
# print(var_value)
error=0
def check_error(input_list):
    global error
    count=1
    count_1=0
    if ['hlt'] not in input_list:
        print("Missing hlt instructions")
        error=1
    for i in input_list:
        if i[0]=='var':
            if var_error(input_list)==1 and count_1==0:
                print("Variable not declared in the beginning")
                error=1
                count_1=1
           
        elif i[0]=='mov':
            if i[1] in register and (i[2]=="FLAGS" or i[2][0]=='$' or i[2] in register):
                continue
            else:
                print("Illegal use of flag register")
                error=1
        elif i[0] not in opcode:
            error=1
            print("Error in line no:"+str(i)+str(copy_list.index(i)+1))
        else:
            newstmtyp=stmtypes[i[0]]
            #print(newstmtyp)
            if newstmtyp=='A':
                for j in i[1:]:
                    if j not in register:
                        error=1
                        print("Invalid Register"+str(i)+str(copy_list.index(i)+1))
                    else :
                        continue
            elif newstmtyp=='B':
                if i[0]=='movf':
                    if float(i[2][1:])>31.5 or float(i[2][1:])<0:
                        error=1
                        print("Invalid Imm value"+str(i)+str(copy_list.index(i)+1))
                else:
                    if i[1] not in register:
                        error=1
                        print("Invalid register"+str(i)+str(copy_list.index(i)+1))
                    elif (i[2][1:].isdigit() and (int (i[2][1:])>127 or int(i[2][1:])<0)):
                        error=1
                        print("Invalid Imm value"+str(i)+str(copy_list.index(i)+1))
            elif newstmtyp=='C':
                for k in i[1:]:
                    if k not in register:
                        error=1
                        print("Invalid Register"+str(i)+str(copy_list.index(i)+1))       
                    else:
                        continue
            elif newstmtyp=="D":
                if i[1] not in register:
                    error=1
                    print("Invalid register"+str(i)+str(copy_list.index(i)+1))
                elif i[2] not in variables:
                    error=1
                    print("Invalid varibale"+str(i)+str(copy_list.index(i)+1))
            elif newstmtyp=="E":
                if i[1] not in labels: 
                    error=1
                    print("label not found "+str(i)+str(copy_list.index(i)+1))
                else:
                    continue
            elif newstmtyp=='F':
                if (copy_list.index(i)+1)<len(copy_list):
                    error=1
                    print("hlt is not being used at last")
                else:
                    continue
            count+=1


check_error(input_list)
   
if error==0:
    binarycode=''
    for i in input_list:
        oprtins=i[0]
        if oprtins=="mov":  # for move 
            if i[2][0]=="$":
                oprtins="mov1"
                
            else:
                oprtins="mov2"
        if oprtins=="var":
            continue
        else:
            newstmtyp=stmtypes[oprtins]
        # print(newstmtyp,oprtins)

        #TYPE A
        if newstmtyp=="A":
            register_1_name = i[1]
            register_2_name = i[2]
            register_3_name = i[3]
            if i[0]== "add":
                binarycode += "0000000"
            elif i[0]== "sub":
                binarycode += "0000100"
            elif i[0]== "mul":
                binarycode += "0011000"
            elif i[0]== "xor":
                binarycode += "0101000"
            elif i[0]== "or":
                binarycode += "0101100"
            elif i[0]== "and":
                binarycode += "0110000"
            elif i[0]== "addf":
                binarycode += "1000000"
            elif i[0]== "subf":
                binarycode += "1000100"
            if register_1_name in register:
                binarycode += register[register_1_name]
            if register_2_name in register:
                binarycode += register[register_2_name]
            if register_1_name in register:
                binarycode += register[register_3_name]
            print(binarycode+"")
            
            binarycode=''
        #TYPE B
        if newstmtyp=="B":
            register_1_name = i[1]
            if oprtins == "mov1":
                binarycode += "000100"
            if oprtins=="movf":
                binarycode += "10010" 
                var=  i[2][1:]
                # print(var)
                decimal= str(var)
                integer,fractional=  decimal.split(".")
                fractional_int=int(fractional)
                # print(integer)
                # print(fractional)
                if register_1_name in register:
                    binarycode += register[register_1_name]
                binary_imm_int = str(bin(int(integer))[2:])
                binary_imm_fra=""
                for j in range(3):
                    fractional_int=int(fractional_int)*2
                    # print(fractional_int)
                    if (int(fractional_int)>=10):
                        binary_imm_fra += "1"
                    else:
                        binary_imm_fra += "0"
                    fractional_int=int(fractional_int)-10
                # print(binary_imm_int)
                # print(binary_imm_fra)
                a=binary_imm_int+binary_imm_fra
                # print(a)
                exponent=int(len(binary_imm_int))-1
                exponent=str(exponent)
                z=bin(int(exponent))
                mantissa=a[1:6]
                mantisa=len(mantissa)
                # print(mantissa)
                if mantisa!=5 and exponent!=3 :
                    exp="0"*(3-len(z[2:]))+z[2:]
                    mn="0"*(5-len(mantissa))+mantissa
                    binarycode+=str(exp)
                    binarycode+=mn
                elif mantisa!=5 and exponent ==3 :
                    exp=a[0:3]
                    mn="0"*(5-len(mantissa))+mantissa
                    binarycode+=str(exp)
                    binarycode+=mn
                elif mantisa==5 and exponent!=3:
                    exp="0"*(3-len(z[2:]))+z[2:]
                    mn=a[1:6]
                    binarycode+=str(exp)
                    binarycode+=mn
                elif mantisa==5 and exponent==3:
                    exp=a[0:3]
                    mn=a[1:6]
                    binarycode+=str(exp)
                    binarycode+=mn
                print(binarycode + "")
            elif i[0]== "rs":
                binarycode += "010000"
            elif i[0]== "ls":
                binarycode += "010010"
            elif oprtins == "mov1" or i[0]== "ls" or "rs":
                if register_1_name in register:
                    binarycode += register[register_1_name]
                binary_imm = str(bin(int(i[2][1:]))[2:])
                binarycode+="0"*(7-len(binary_imm))+binary_imm
                print(binarycode + "")
            binarycode=''
        # imm value

        #TYPE C
        if newstmtyp=="C":
            register_1_name = i[1]
            register_2_name = i[2]
            if oprtins == "mov2":
                binarycode += "0001100000"
            elif i[0]== "div":
                binarycode += "0011100000"
            elif i[0]== "not":
                binarycode += "0110100000"
            elif i[0]== "cmp":
                binarycode += "0111000000"    
            if register_1_name in register:
                binarycode += register[register_1_name]
            if register_2_name in register:
                binarycode += register[register_2_name]
            print(binarycode +"")
            binarycode=''
        #TYPE D
        if newstmtyp=="D":
            register_1_name = i[1]
            if i[0] == "ld":
                binarycode += "001000"
            elif i[0]== "st":
                binarycode += "001010"
            if register_1_name in register:
                binarycode += register[register_1_name]
            binarycode+= var_value[(variables.index(i[2]))]
            print(binarycode +"")
            binarycode=''
        #TYPE E
        if newstmtyp == 'E':
            if i[0] == "jmp":
                binarycode += "011110000"
            elif i[0]== "jlt":
                binarycode += "111000000"
            elif i[0]== "jgt":
                binarycode += "111010000"
            elif i[0]== "je":
                binarycode += "111110000"
            binarycode+= labels_val[(labels.index(i[1]))]
            print(binarycode +"")
            binarycode=''
        #TYPE F
        if newstmtyp=='F':
            binarycode+="1101000000000000"
            print(binarycode+"")
            
# print(binarycode)
# print(labels)
