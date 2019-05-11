import pandas as pd

def gen_csv(self,filename):
        df = pd.read_csv(filename)
        for i in df.iloc[:,1]:
            yield utils.clr(str(i).strip())
        #for i in rand_lst(len(df.iloc[:,1]),self.batch):
        #    yield utils.clr(str(df.iloc[i,1].strip()))

def gen_txt(self,filename):
        f = open(filename,'r')
        lines = f.readlines()
        for i in lines:
            yield utils.clr(str(i).strip())
        #for i in rand_lst(len(lines),self.batch):
        #    yield strQ2B(str(lines[i].strip()))

