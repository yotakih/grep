#-*- coding: utf-8 -*-

import glob
import io
import os
import re
import sys
import shutil

dlm='\t'
enc=65001

def wrt_grp(p:str,lst_re:list,w_out_grp,w_out_cnt)->list:
    txt=''
    lst_cnt=[0]*len(lst_re)
    with open(p,'r',enc) as r:
        txt=r.read()
    for ln in txt.splitlines():
        lnOutFlg=False
        for i in range(len(lst_re)):
            ptn:re.Pattern=lst_re[i]
            cnt=len(ptn.findall(ln))
            lst_cnt[i]+=cnt
            if cnt>0 and not lnOutFlg:
                w_out_grp.write(dlm.join([p,os.path.basename(p),ln])+'\n')
                lnOutFlg=True
    w_out_cnt.write(dlm.join([p,os.path.basename(p)]+[str(x) for x in lst_cnt])+'\n')
    return lst_cnt

def glob_ext(fldr:str,ext:str)->str:
    for p in glob.glob(r'{}/**/*{}'.format(fldr,ext),recursive=True):
        yield p

def create_re_kywds(fl_kywds:str)->list:
    txt=''
    with open(fl_kywds,'r',enc) as r:
        txt=r.read()
    return [re.compile(ptn) for ptn in txt.splitlines() if ptn.strip()!='']

def create_w_out_cnt(out_cnt:str,lst_re:list)->io.BufferedWriter:
    w=open(out_cnt,'w',enc)
    w.write(dlm.join(['full path','file name']+lst_re)+'\n')
    return w

def create_w_out_grep(out_grp:str)->io.BufferedWriter:
    w=open(out_grp,'w',enc)
    w.write(dlm.join(['full path','file name','grep result'])+'\n')
    return w

def proc(fldr:str,ext:str,fl_kywds:str,out_grp:str,out_cnt:str):
    lst_re=create_re_kywds(fl_kywds)
    w_out_grp=create_w_out_grep(out_grp)
    w_out_cnt=create_w_out_cnt(out_cnt,[ptn.pattern for ptn in lst_re])
    [wrt_grp(p,lst_re,w_out_grp,w_out_cnt) for p in glob_ext(fldr,ext)]

def analize_args(lst_args)->list:
    if len(lst_args)!=5:
        print('usage:')
        print(' arg1:grep dir')
        print(' arg2:grep extension')
        print(' arg3:grep keywords file path')
        print(' arg4:result grep file path')
        print(' arg5:result grep cnt file path')
        sys.exit()
    return lst_args

def main(lst_args):
    proc(*analize_args(lst_args[1:]))

def test():
    test_root_dir='test'
    os.mkdir(test_root_dir)
    kywdsfl=os.path.join(test_root_dir,'keywords.txt')
    with open(kywdsfl,'w') as w:
        w.write(r'^hoge.*fuga$'+'\n')
        w.write(r'.*piyo.*'+'\n')
    grep_dir=os.path.join(test_root_dir,'grepdir')
    os.mkdir(grep_dir)
    with open(os.path.join(grep_dir,'test1.xml'),'w') as w:
        w.write('hoge piyo fuga\n')
        w.write('fuga\n')
    grep_dir_chld=os.path.join(grep_dir,'child')
    os.mkdir(grep_dir_chld)
    with open(os.path.join(grep_dir_chld,'test2.xml'),'w') as w:
        w.write('hoge piyo fuga\n')
        w.write('fuga\n')
    with open(os.path.join(grep_dir_chld,'test3.xml'),'w') as w:
        w.write('fuga\n')
    with open(os.path.join(grep_dir_chld,'test4.txt'),'w') as w:
        w.write('hoge piyo fuga\n')
        w.write('fuga\n')
    outgrepfl=os.path.join(test_root_dir,'outgrep.tsv')
    outcntfl=os.path.join(test_root_dir,'outcnt.tsv')
    proc(grep_dir,'.xml',kywdsfl,outgrepfl,outcntfl)
    print('grep result file:')
    with open(outgrepfl,'r') as r:
        print(r.read())
    with open(outcntfl,'r') as r:
        print(r.read())
    shutil.rmtree(test_root_dir)

if __name__=='__main__':
    main(sys.argv)
#    test()
