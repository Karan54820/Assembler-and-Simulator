import sys
temp_list=[]
output_list=[]

opcode={'add':'00000','sub':'00001','mov1':'00010','mov2':'00011','ld':'00100','st':'00101',
        'mul':'00110','div':'00111','rs':'01000','ls':'01001','xor':'01010','or':'01011',
        'and':'01100','not':'01101','cmp':'01110','jmp':'01111','jlt':'11100','jgt':'11101',
        'je':'11111','hlt':'11010',"movf":"10010",'addf':'10000','subf':'10001'}

stmtypes = {"add": "A", "sub": "A", "mov1": "B", "mov2": "C", "ld": "D", "st": "D", 
            "mul": "A", "div": "C", "rs": "B","ls": "B", "xor": "A", "or": "A",
             "and": "A", "not": "C", "cmp": "C", "jmp": "E", "jlt": "E", "jgt": "E",
             "je": "E", "hlt": "F","movf":"B",'addf':'A','subf':'A'}

variables=[]
var_value=[]
flags = {'V': 0, 'L': 0, 'G': 0, 'E': 0}
register={'000':0,'001':0,'010':0,'011':0,'100':0,'101':0,'110':0,"111":0}

opcode_typedict={'A':2,'B':1,'C':5,'D':1,'E':4,'F':11}
def floatconvert(binary):
    exponent = binary[:3]
    mantissa = binary[3:]
    if exponent=="000" and mantissa=="00000":
        value=0.0
        return value
    elif exponent=="111" and mantissa=="00000":
        print("Error")
        return 
    elif int(exponent,2)<=6 and int(exponent,2)>=1:
        exponent = int(exponent, 2) - 3
        mantissa_val = 0.0
        for i in range(5):
            mantissa_val += int(mantissa[i]) * 2 ** -(i + 1) 
        #floating-point value
        value = (1 + mantissa_val) * (2 ** exponent)
        return value
    elif exponent=="000" and int(mantissa,2)!=0:
        mantissa_val = 0.0
        for i in range(5):
            mantissa_val += int(mantissa[i]) * 2 ** -(i + 1)
        value=mantissa_val
        return value
    elif exponent=="111" and int(mantissa,2)!=0:
        print("Error")
        return 

def convert(register):
    binary_register = {}
    binary_register1 = {}
    for key, value in register.items():
        binary_value = bin(value)[2:].zfill(16)
        binary_value1 = bin(value)[2:].zfill(16)
        binary_register[key] = binary_value[8:]
    return binary_register
# f=open("test_result.txt")

def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

s=sys.stdin.read()
f=s.split("\n")
for line in f:
    line =line.strip()
    if not  line:
        continue #remove whit e
    splt=[splt.strip() for splt in line.split()]
    temp_list.append(splt)# splititng into variable ....

for i in (temp_list):
    output_list.append(i[0])

# print(output_list)
for i in output_list:
    pc_val="{0:07b}".format(output_list.index(i))
    opcode_val=i[0:5]

    if opcode_val=="00100" or opcode_val=="00101":
        variable_code=i[9:]
        if variable_code not in variables:
            variables.append(variable_code)
            var_value.append(0)

copy_list=output_list.copy()
pc_val=0
halt=False
input_list=[]
index=0
i=output_list[0]
while(not halt):
    # index=0
    # print(output_list.index(i),pc_val)
    if output_list.index(i)==pc_val:
        for i in output_list[pc_val:]:
            opcode_val=i[0:5]
            opcode_1=get_key_from_value(opcode,opcode_val)
            # print(opcode_1)
            opcode_type=stmtypes[opcode_1]
            # print(opcode_type)
            # print(opcode_1)
            unused_bits=opcode_typedict[opcode_type]

            if opcode_type=='A':
                    A1=i[7:10]
                    A2=i[10:13]
                    A3=i[13:16]
                    # print(A1,A2,A3)
                    if opcode_1=="add":
                        register[str(A1)]=register[str(A2)]+register[str(A3)]
                        # print(bin(register[str(A1)])[2:])
                        if len(bin(register[str(A1)])[2:])>16:
                            flags['V']=1
                            register[str(A1)]=0

                    elif opcode_1=="sub":
                        register[str(A1)]=register[str(A2)]-register[str(A3)]
                        if register[str(A1)]<0:
                            flags['V']=1
                            register[str(A1)]=0

                    elif opcode_1=="mul":
                        register[str(A1)]=register[str(A2)]*register[str(A3)]
                        if len(bin(register[str(A1)]))>16:
                            flags['V']=1
                            register[str(A1)]=0

                    elif opcode_1=="xor":
                        register[str(A1)]=register[str(A2)]+register[str(A3)]    

                    elif opcode_1=="or":
                        # print(int("{0:07b}".format((register[str(A2)]))))
                        register[str(A1)]=register[str(A2)] | register[str(A3)]

                    elif opcode_1=="and":
                        register[str(A1)]=register[str(A2)] & register[str(A3)]
                    # print(register)
                    pc_val+=1
            if opcode_type=="B":
                btype=i[6:16]
                reg1=btype[0:3]
                imm1=btype[3:10]
                # print(reg1,imm1)
                if opcode_1=="mov1":
                    register[str(reg1)]=int(imm1,2)
                    # print(register)

                elif opcode_1=="rs":
                    # print(int(imm1,2))
                    register[str(reg1)]=int(register[str(reg1)]/(2**(int(imm1,2))))
                    # print(register)

                elif opcode_1=="ls":
                    register[str(reg1)]=int(register[str(reg1)](2*(int(imm1,2)))) 
                    # print(register)
                pc_val+=1
            if opcode_type=="C":
                ctype=i[10:16]
                # print(ctype)
                A1=ctype[0:3]
                A2=ctype[3:6]
                if opcode_1=="cmp":
                    if register[str(A1)]<register[str(A2)]:
                        flags['L']=1

                    elif register[str(A1)]>register[str(A2)]:
                        flags['G']=1

                    elif register[str(A1)]==register[str(A2)]:
                        flags['E']=1
                    temp=""
                    temp+=str(flags["V"])
                    temp+=str(flags["L"])
                    temp+=str(flags["G"])
                    temp+=str(flags["E"])
                    # register[str(A1)]=int(temp,2)
                    register["111"]=int(temp,2)

                elif opcode_1=="mov2" and A2=="111":
                    temp=""
                    temp+=str(flags["V"])
                    temp+=str(flags["L"])
                    temp+=str(flags["G"])
                    temp+=str(flags["E"])
                    register[str(A1)]=int(temp,2)
                    # register["111"]=int(temp,2)

                elif opcode_1=="mov2":
                    register[str(A1)]=register[str(A2)]

                elif opcode_1=="div":
                    register["000"]=register[str(A1)]//register[str(A2)]
                    register["001"]=register[str(A1)]%register[str(A2)]
                    
                elif opcode_1=="not":
                    register[str(A1)]= ~register[str(A2)]
                
                
                pc_val+=1
                # print(register)
                # print(flags)
                # print(A1,A2)    

            if opcode_type=="D":
                dtype=i[6:16]
                # print(dtype)
                A1=dtype[0:3]
                A2=dtype[3:10]

                if opcode_1=="ld":
                    # print(variables.index(A2))
                    register[str(A1)]=var_value[variables.index(A2)] 
                    # print(var_value)
                
                elif opcode_1=="st":
                    var_value[variables.index(A2)]=register[str(A1)]
                    # print(var_value)
                pc_val+=1

            if opcode_type=="E":
                A1=i[9:]
                # print(A1)
                if opcode_1=='jmp':
                        # pc_val+=1
                        print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
                        pc_val=int(A1,2)
                        # print(pc_val)
                        break
                elif opcode_1=="jlt":
                    if flags['L']==1:
                        pc_val+=1
                        print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
                        pc_val=int(A1,2)
                        break
                    else:
                        pc_val+=1
                elif opcode_1=="jgt":
                    if flags['G']==1:
                        pc_val+=1
                        print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
                        pc_val=int(A1,2)
                        # print(pc_val)
                        break
                    else:
                        pc_val+=1
                elif opcode_1=="je":
                    if flags['E']==1:
                        pc_val+=1
                        print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
                        pc_val=int(A1,2)
                        break
                    else:
                        pc_val+=1

            if opcode_type=="F":
                # print(1)
                ftype=i[5:16]
                halt=True
                pc_val+=1
                print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
                break
            # print(pc_val-1)
            # print(register)
            print("{0:07b}".format(pc_val-1),"{0:016b}".format(register["000"]),"{0:016b}".format(register["001"]),"{0:016b}".format(register["010"]),"{0:016b}".format(register["011"]),"{0:016b}".format(register["100"]),"{0:016b}".format(register["101"]),"{0:016b}".format(register["110"]),"{0:016b}".format(register["111"]))
            register["111"]=0
            # print(register)

            
            binary_register = convert(register)
            # print(binary_register)
            br1 = {}
            for key, value in register.items():
                if key in binary_register:
                    binary_value = binary_register[key]
                    floating_point_value = floatconvert(binary_value)
                    br1[key] = floating_point_value
            # print(br1)
    else:
        
        if index>len(output_list):
            index=0
        else:
            index+=1
            #print(len(copy_list))
            i=copy_list[index]
            # print(i)
            
        # print(i)           


         
for i in output_list:                      
    opcode_val=i[0:5]
    A1=i[7:10]
    A2=i[10:13]
    A3=i[13:16]
    if opcode_val=="10000":
        for key,value in br1.items():
            if A1 and A2 and A3 in key:
                A=br1[A1]
                B=br1[A2]
                C=br1[A3]
                A=B+C
                # print(A)  
                if (A) > 31.5:  #of bits by which we have to cpmare  
                    flags['V']=1
                    A = 0  
                br1[A1] = A 
    elif opcode_val=="10001":
        for key,value in br1.items():
            if A1 and A2 and A3 in key:
                A=br1[A1]
                B=br1[A2]
                C=br1[A3]
                A=B-C 
                if int(B,2)<int(C,2):  #of bits by which we have to cpmare  
                    flags['V']=1
                    A = 0  
                br1[A1] = A 
    elif opcode_val=="10010":
        for key,value in br1.items():
            if A1 in key:
                A=br1[A1]
                imm=i[8:16]
                floating=int(imm,2)
            br1[A1]=A
