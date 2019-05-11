#!encoding=utf8

def init_base_dict():
    """  
    this product the unit words for normal cell, like floor room building
    """
    with open("./ll.txt","a+") as f:
        for i in ["A","B","C","D","E","F",""]:
            for j in range(100):
                for m in range(['楼','号楼','楼层','层','号院'])
                    f.write("%s%s%s nz 9999\n"%(i,j,m))



