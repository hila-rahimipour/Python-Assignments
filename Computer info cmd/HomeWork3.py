"""
Author: Hila Rahimipour
homework exercise 3
The program analyses "ipconfig/ all" and prints tables of NIC's (name, state, physical address, DHCP enable)
and IP's (ip, gateway, host)
"""
#importing subprocess and texttable in order to run the command and print the tables 
import subprocess
import texttable

#creating connection and running command
def run_command(cmd):
    return subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE, stdin = subprocess.PIPE).communicate()

#creating the variables of the table and organizing the collected date ("ipconfig/ all)
output = run_command("ipconfig /all")[0].decode(errors = "replace").split("\r\n")

names_nic = ["Name"]
state_nic = ["State"]
mac_nic = ["Physical Address"]
DHCP_nic = ["DHCP Enabled"]
index_nic = -1

ip = ["IPv4 Address"]
gateway = ["GateWay"]
host = ["HostName"]
index_ip = -1

#adding and analyzing the information in the command to the lists of the tables' value
#Nic information analyzing
for i in range(len(output)):
    if "adapter" in output[i]:
        names_nic.append(output[i])
        index_nic = i
    if not index_nic == -1:
        for j in range(index_nic, len(output)):
            check = False
            if "State" in output[i]:
                if "disconnected" in output[i]:
                    state_nic.append("disconnected")
                    break
                else:
                    state_nic.append("connected")
                    break
            if "IPv4" in output[i]:
                check = True
            if "Physical Address" in output[i]:
                mac_nic.append(output[i][39:])
                break
            if "DHCP Enabled" in output[i] and "Yes" in output[i]:
                DHCP_nic.append("Yes")
                break
            if "DHCP Enabled" in output[i] and "No" in output[i]:
                DHCP_nic.append("No")
                break
            if check:
                state_nic.append("connected")
                break
    #IP information analyzing
    
    if "IPv4 Address" in output[i]:
        ip.append(output[i][39:output[i].find("(")])
        index_ip = i
    if not index_ip == -1:
        for j in range(index_ip, len(output)):
            if "Gateway" in output[i]:
                gateway.append(output[i][39:])
                break
    if "Host Name" in output[i]:
        host.append(output[i][39:])
        
print("Computer Information:\n")        
#creating and printing table for NIC information
table_nic = texttable.Texttable(100)
table_nic.add_row(["Computer Information: NIC", "", "", ""])
for i in range(len(names_nic)):
    table_nic.add_row([names_nic[i], mac_nic[i], state_nic[i], DHCP_nic[i]])
print(table_nic.draw()+"\n")

#creating and printing table for IP information
table_ip = texttable.Texttable()
table_ip.add_row(["Computer Information: IP", "", ""])
for i in range(len(ip)):
    table_ip.add_row([ip[i], gateway[i], host[i if i < 2 else 1]])
print(table_ip.draw())

#adding information from systeminfo if the client wants
system_info = input("do you want to compare with systeminfo? y/n: ")
while not system_info == 'y' and not system_info == 'n':
    print("please answer y/n")
    system_info = input("do you want to compare with systeminfo? y/n: ")
if system_info == 'y':
    output = run_command("systeminfo")[0].decode(errors = "replace").split("\r\n")
    for i in range(len(output)):
        if "Host Name" in output[i]:
            print(f'\nyour Host Name is {output[i][27:]}')
        if "System Manufacturer" in output[i]:
            print(f'your System Manufacturer is {output[i][27:]}')
        if "System Model" in output[i]:
            print(f'your System Model is {output[i][27:]}')
        if "NIC" in output[i]:
            print(f'the amout of NIC\'s you have in your computer: {output[i][27:output[i].find("NIC")]}')





            
