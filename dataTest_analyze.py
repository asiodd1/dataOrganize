import json

'''
with open('TEST_DATA.txt', mode='r') as fh:
    data_all = fh.readlines()

for line in data_all:
    if 'SLOTS' in line:
'''
def make_dataStream(fh):
    line = fh.readline()
    fh.seek(0)
    data_stream = {}
    i = 0

    while line != '':
        
        line = fh.readline()
        if 'SLOTS' in line:
            i = i+1
            line = line[line.find('SLOTS')+6:]
            data_stream['execution'+str(i)] = {}
            data_stream['execution'+str(i)]['SLOTS'] = line[:line.find(']')]

            line = line[line.find('TICK')+5:]
            data_stream['execution'+str(i)]['TICK'] = line[:line.find(']')]

            line = line[line.find('EXECUTING')+10:]
            data_stream['execution'+str(i)]['EXECUTING'] = line[:line.find(']')]

            line = fh.readline()#再讀一行
            
            line = line[line.find('CRC_GOOD')+10:]
            data_stream['execution'+str(i)]['CRC_GOOD'] = line[:line.find(']')]

            line = line[line.find('CRC_BAD')+8:]
            data_stream['execution'+str(i)]['CRC_BAD'] = line[:line.find(']')]

            line = fh.readline()#next line

            line = line[line.find('ACK')+5:]
            data_stream['execution'+str(i)]['ACK'] = line[:line.find(']')]

            line = line[line.find('NACK')+5:]
            data_stream['execution'+str(i)]['NACK'] = line[:line.find(']')]

            line = fh.readline()#next line

            line = line[line.find('Drtx')+9:]
            data_stream['execution'+str(i)]['Drtx'] = {}
            data_stream['execution'+str(i)]['Drtx']['1st'] = line[:line.find(']')]

            line = line[line.find('2nd')+4:]
            data_stream['execution'+str(i)]['Drtx']['2nd'] = line[:line.find(']')]

            line = line[line.find('3rd')+4:]
            data_stream['execution'+str(i)]['Drtx']['3rd'] = line[:line.find(']')]

            line = line[line.find('Fail')+5:]
            data_stream['execution'+str(i)]['Drtx']['rtx Fail'] = line[:line.find(']')]

            line = fh.readline()#next line

            line = line[line.find('Urtx')+9:]
            data_stream['execution'+str(i)]['Urtx'] = {}
            data_stream['execution'+str(i)]['Urtx']['1st'] = line[:line.find(']')]

            line = line[line.find('2nd')+4:]
            data_stream['execution'+str(i)]['Urtx']['2nd'] = line[:line.find(']')]

            line = line[line.find('3rd')+4:]
            data_stream['execution'+str(i)]['Urtx']['3rd'] = line[:line.find(']')]

            line = line[line.find('Fail')+5:]
            data_stream['execution'+str(i)]['Urtx']['rtx Fail'] = line[:line.find(']')]
    return data_stream

#def main():
fh = open('TEST_DATA.txt', mode= 'r')
data_stream = make_dataStream(fh)
fh.close()
#print(data_stream)
gh = open('TEST_DATA_analyzedToJson.txt','w')
gh.write(json.dumps(data_stream))
gh.close()
vh = open('TEST_DATA_analyzedToTable.txt','w')
for key in data_stream:
    vh.write(key+'  SLOTS: '+data_stream[key]['SLOTS']+'  TICK: '+data_stream[key]['TICK']+'  EXECUTING:'+data_stream[key]['EXECUTING']+'  CRC_GOOD: '+data_stream[key]['CRC_GOOD']+'  CRC_BAD: '+data_stream[key]['CRC_BAD']+'  ACK: '+data_stream[key]['ACK']+'  NACK: '+data_stream[key]['NACK']+'  Drtx: '+data_stream[key]['Drtx']['1st']+','+data_stream[key]['Drtx']['2nd']+','+data_stream[key]['Drtx']['3rd']+',Fail='+data_stream[key]['Drtx']['rtx Fail']+'  Urtx: '+data_stream[key]['Urtx']['1st']+','+data_stream[key]['Urtx']['2nd']+','+data_stream[key]['Urtx']['3rd']+',Fail='+data_stream[key]['Urtx']['rtx Fail']+'\n')
vh.close()

print('總共執行次數'+str(len(data_stream)))
print('起始時間: '+str(int(data_stream['execution1']['EXECUTING'])//60)+'分'+str(int(data_stream['execution1']['EXECUTING'])%60)+'秒')
print('結束時間: '+str(int(data_stream['execution'+str(len(data_stream))]['EXECUTING'])//60)+'分'+str(int(data_stream['execution'+str(len(data_stream))]['EXECUTING'])%60)+'秒')


while True:
    check = input('檢查選項:CRC_BAD/NACK?')
    if check == 'CRC_BAD':
        badlimit = int(input('欲檢查CRC_BAD大於多少的資料? '))
        for key in data_stream:
            if int(data_stream[key]['CRC_BAD']) > badlimit:
                print(str(int(data_stream[key]['EXECUTING'])//60)+'分'+str(int(data_stream[key]['EXECUTING'])%60)+'秒'+' '+key+' CRC_BAD='+data_stream[key]['CRC_BAD']+' Urtx='+str(data_stream[key]['Urtx']))
    elif check == 'NACK':
        nacklimit = int(input('欲檢查NACK大於多少的資料? '))
        for key in data_stream:
            if int(data_stream[key]['NACK']) > nacklimit:
                print(str(int(data_stream[key]['EXECUTING'])//60)+'分'+str(int(data_stream[key]['EXECUTING'])%60)+'秒'+' '+key+' NACK='+data_stream[key]['NACK'])

    else:
        print('請重新輸入:(CRC_BAD/NACK)')
#main()
