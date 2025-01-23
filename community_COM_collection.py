import pandas as pd
import os
import sys
def COM_collection(COM_list):
    _id=[]
    X=[]
    Y=[]
    Z=[]
    folder=os.listdir(COM_list)
    if os.path.exists(COM_list+'/'+'.DS_Store'):
        folder.remove('.DS_Store')
    else:
        print("DS_store does not exist.")
    for i in folder:
        print(i)
        with open(COM_list+'/'+i,'r') as f:
            contents=f.readlines()
            print(contents)
            parts=str(contents).split(' ')
            id_=parts[0]
            print(id_)
            id_=id_.replace('[','')
            id_=id_.replace("'","")
            parts[1]=parts[1].replace('[','')
            parts[1]=parts[1].replace(',','')
            parts[2]=parts[2].replace(',','')
            parts[3]=parts[3].replace(']','')
            parts[3]=parts[3].replace("'","")
            parts[3]=parts[3].replace('\\n','')
            _id.append(id_)
            X.append(parts[1])
            Y.append(parts[2])
            Z.append(parts[3])
    df=pd.DataFrame()
    df['community_id']=_id
    df['X']=X
    df['Y']=Y
    df['Z']=Z
    return df

if __name__=='__main__':
    COM_list=sys.argv[1]
    df=COM_collection(COM_list)
    df.to_csv(sys.argv[2])
