import sys,os,math,re,traceback,datetime

if (len(sys.argv)==1 or sys.argv[0].find("help")>-1):
    print "python2 times"
    die

dir=re.split("[ \n]",sys.argv[1])
ext=sys.argv[2]
type=sys.argv[3]
printing=True
percent=False
overAll=True
link=False

if(dir[0]==""):
    dir.pop(0)

#print "looking at "+str(dir)

i=3
# print minimal output only
while(len(sys.argv)>i):
    if(sys.argv[i]=="--essentials" or sys.argv[i]=="--e"):
        printing=False
    if(sys.argv[i]=="--percent" or sys.argv[i]=="--p"):
        percent=True
    if(sys.argv[i]=="--noOverAll" or sys.argv[i]=="--n"):
        overAll=False
    if(sys.argv[i]=="--link" or sys.argv[i]=="--l"):
        link=True      
    i+=1

if (dir == ["all"]):
    dir=[]
    for f in os.listdir('.'):
        if(f[-5::]=="_seqs"):
            if(type=="snpFilter"):
                dir.append(f+"/snp")
            else:
                dir.append(f+"/aln")
#if(printing):
#   print dir

names=[]


def average(arr):
    sum=0
    for a in arr:
        sum+=float(a)
    sum/=len(arr)
    return(sum)

def std(arr,av):
    sum=0
    for a in arr:
        sum+=(float(a)-float(av))*(float(a)-float(av))
    sum=math.sqrt(sum/(len(arr)))
    return(sum)

def ste(arr):
    av=average(arr)
    return(std(arr,av)/math.sqrt(len(arr)))

def per(max,arr):
    sum=0
    for a in range(0,len(arr)):
        if (float(arr[a])!=0.0):
            sum+=float(arr[a])/float(max[a])
    if (sum==0.0):
        return 0
    sum/=len(arr)
    return sum


def printStats(arrV, arrN, arrS):
    out=[[],[],[],[],[]]
    string="    "
    for c in range(0,len(arrV)):
        string+="%17s " % arrN[c]
        formatString="%17.2f"
        if(min(arrV[c])<0.009):
            formatString="%17.2e"
            #formatString="%17.2f"
        out[0].append(formatString % (min(arrV[c])))
        out[1].append(formatString % (max(arrV[c])))
        out[2].append(formatString % (average(arrV[c])))
        out[3].append(formatString % (ste(arrV[c])))
        if (percent):
            out[4].append(formatString % (per(arrV[0],arrV[c])))
    if(printing and arrS!=0 ):
        print string
        for l in arrS:
            resultPerS="    "
            for e in l[0]:
                formatString="%17.2f "
                if(e<0.009):
                    formatString="%17.2e "
                resultPerS+= formatString % e
            resultPerS+=" "+l[1]
            print resultPerS
        if(arrS==0 or len(arrS)>1):    
            print "-----------------------------"
    if(arrS==0 or len(arrS)>1):
        print string
        print "min "+" ".join(out[0])
        print "max "+" ".join(out[1])
        print " av "+" ".join(out[2])
        print "ste "+" ".join(out[3])
        if (percent):
            print "av% "+" ".join(out[4])
            

# sam statiscis for initial aligment
def samstats_old(statsfile):
    names=["total","QCfail","dupl","dupl%","mapped","maped%","paired", "paired%", "singletons", "transv", "regmapped", "regmapped%", "regpaired", "regpaired%"]
    values=[]
    st=re.split("[ \n]+",open(statsfile).read())
    #print st
    values.append(int(st[0])) # total
    values.append(int(st[3])) # QCfail
    values.append(int(st[6])) # dupl
    values.append(float(st[6])/float(st[0])) # dupl%
    values.append(int(st[8])) # mapped
    values.append(float(values[-1])/values[0]) # mapped %
    values.append(int(st[19])) # paired
    values.append(float(values[-1])/values[0]) # paired %
    values.append(int(st[29]))
    values.append(int(st[40]))
    if (len(st)>50):
        values.append(int(st[51])) # regmapped
        values.append(float(values[-1])/values[0]) 
        values.append(int(st[56]))
        values.append(float(values[-1])/values[0])
    #if(printing):
    #    string="    "
    #    for v in values:
    #        string+="%16.2f" % v
    #    print string+" "+statsfile
    return names,values


# sam statiscis for initial aligment
def samstats(statsfile):
    names=["total","QCfail","dupl","dupl%","mapped","maped%","paired", "paired%", "singletons", "regmapped", "regmapped%", "regpaired", "regpaired%"]
    values=[]
    st=re.split("[ \n]+",open(statsfile).read())
    #sys.stderr.write(",".join(st))
    values.append(int(st[0])) # total
    values.append(int(st[2])) # QCfail
    values.append(int(st[10])) # dupl
    values.append(float(values[-1])/float(values[0])) # dupl%
    values.append(int(st[14])) # mapped
    values.append(float(values[-1])/float(values[0])) # mapped %
    values.append(int(st[33])) # paired
    values.append(float(values[-1])/float(values[0])) # paired %
    values.append(int(st[47]))
    if (len(st)>75):
        values.append(int(st[75])) # regmapped
        values.append(float(values[-1])/values[0]) 
        values.append(int(st[80]))
        values.append(float(values[-1])/values[0])
    return names,values




# sam statiscis for initial aligment
def tophat(statsfile):
    names=["total","accepted","QCfail","dupl","dupl%","mapped","maped%","paired", "paired%", "singletons"]
    values=[]
    st=re.split("[ \n]+",open(statsfile).read())
#    print st
    values.append(int(st[73])) # total
    values.append(int(st[0])) # acepted
    values.append(int(st[2])) # QCfail
    values.append(int(st[10])) # dupl
    values.append(float(values[-1])/float(values[0])) # dupl%
    values.append(int(st[14])) # mapped
    values.append(float(values[-1])/float(values[0])) # mapped %
    values.append(int(st[33])) # paired
    values.append(float(values[-1])/float(values[0])) # paired %
    values.append(int(st[47]))
    if (len(st)>76):
        names.append("junction")
        names.append("junction %")
        names.append("jnct over ncbi")
        names.append("jnct over ncbi %")
        values.append(int(st[76])) # junction reads
        #values.append(float(values[-1])/float(values[5])) # junction %
        values.append(float(values[-1])/float(values[0])) # junction %
        values.append(int(st[79])) # junction reads in ncbi genes
        values.append(float(values[-1])/float(values[10])) # junction reads in ncbi genes %
        
    return names,values


def onTarget(statsfile):
    names=["total", "paired total", "paired total(%)" ,"onTargt 100","(%)", "paired oT 100","(%)"]
    values=[]
    f=open(statsfile).read()
#    print f
    st=re.split("[ \n]+",f)
#    print st
#    print st[205]
    values.append(int(st[75])) # total
    values.append(int(st[85])) # paired total
    values.append(float(values[-1])/float(values[0])) # paired total %
    values.append(int(st[0])) # on target
    values.append(float(values[-1])/float(values[0])) # on taget %
    values.append(int(st[33])) # paired
    values.append(float(values[-1])/float(values[0])) # paired %
    if (f.find("# on target 0")>-1):
        names.append("pairedd oT 200")
        names.append("(%)")
        names.append("paired oT 0")
        names.append("(%)")
        values.append(int(st[205])) # on target 200
        values.append(float(values[-1])/float(values[0])) # on taget 200 %
        values.append(int(st[128])) # on target 0
        values.append(float(values[-1])/float(values[0])) # on taget 0 %
        
    return names,values



def time(file):
    st=open(file).read()
    start=datetime.datetime.strptime(st.split(">>>>> startdate ")[1].split("\n")[0], "%a %b %d  %H:%M:%S EST %Y")
    end=datetime.datetime.strptime(st.split(">>>>> enddate ")[1].split("\n")[0], "%a %b %d  %H:%M:%S EST %Y")
    delta=end-start
    return ["seconds", "hours"],[delta.total_seconds(),delta.total_seconds()/(60*60)]


# sam statistics for recalibrated scores and realigned bams
def samstatsrecal(statsfile):
    # properties of the recalibrated file
    names,values = samstats (statsfile)

    # properties of the initial files
    n,valun = samstats(statsfile.replace(".recal.clean", ""))

    names+=["imprpaired"]
    values.append(valun[5]-values[5])
#    print valun
#    print values
    if (len(valun)>9 and len(values)>9):
        names+=["imprregpaired"]
        values.append(valun[9]-values[9])
    return names,values
    

# sam statiscis for initial aligment
def bamDist(bamfile, col):

    names=[]
    values=[]
    pre=""
    if(col==1):
        pre="mapped"
    elif(col==5):
        pre="pqal20"

    st=os.popen3("python ../bin/bamchromdist.py "+bamfile)[1].read().split("\n")
    
    for s in st[2:-3]:
        arr=re.split("[ \t]+",s)
        if(arr[0]==""):
            arr.pop(0)
        names.append(pre+"_"+arr[0])
        values.append(int(arr[col]))
    if(printing):
        print str(values)+" "+bamfile
    return names,values


def variant(variantFile):
    names=["Total","known", "SNPdb Conc", "Ti/Tv", "Het/Hom", "novel", "Ti/Tv","Het/Hom"]
    values=[]
    file=open(variantFile).read()
    CO=file.split("CompOverlap :")[1].split("##")[0].split("\n")
    snpdb=len(CO)-5
    CV=file.split("CountVariants :")[1].split("\n")
    TI=file.split("TiTvVariantEvaluator :")[1].split("\n")
    #print re.split("[ \t]+",CV[1])
    #print re.split("[ \t]+",CV[1])[25]
    #print re.split("[ \t]+",CV[3])[25]
    number=11
    number2=24
    if (CO[1].find("nCompVariants")==-1):
        number=10
    if (CV[1].find("nMixed")>-1):
        number2=25
    values.append(int(re.split("[ \t]+",CO[snpdb])[5])) #all
    values.append(int(re.split("[ \t]+",CO[snpdb+1])[5])) #known
    values.append(float(re.split("[ \t]+",CO[snpdb+1])[number])) #concKnown
    values.append(float(re.split("[ \t]+",TI[snpdb+1])[7])) #Ti/Tv known
    values.append(float(re.split("[ \t]+",CV[snpdb+1])[number2])) #Het/Hom known
    values.append(int(re.split("[ \t]+",CO[snpdb+2])[5])) #novel
    values.append(float(re.split("[ \t]+",TI[snpdb+2])[7])) # Ti/Tv novel
    values.append(float(re.split("[ \t]+",CV[snpdb+2])[number2])) # Het/Hom novel
    if (file.find("MendelianViolationEvaluator :")>-1):
        ME=file.split("MendelianViolationEvaluator :")[1].split("\n")
        names.append("EvalVariants")
        names.append("errors")
        names.append("Right/Wrong")
        names.append("HomVarP2HomRefK")
        names.append("HomRefP2HetK")
        names.append("HomVarP2HetK")
        names.append("HomRefP2HomVarK")
        values.append(float(re.split("[ \t]+",ME[snpdb])[5])) #evaluated Variants
        values.append(float(re.split("[ \t]+",ME[snpdb])[6])) #all errors
        values.append((values[-1]/values[-2])*100)
        values.append(float(re.split("[ \t]+",ME[snpdb])[7])) #all errors
        values.append(float(re.split("[ \t]+",ME[snpdb])[8])) #all errors
        values.append(float(re.split("[ \t]+",ME[snpdb])[9])) #all errors
        values.append(float(re.split("[ \t]+",ME[snpdb])[10])) #all errors
        
    i=2
    while (i!=snpdb):
        arr=re.split("[ \t]+",CO[i])
        names.append(arr[1]+" rate")
        names.append(arr[1]+" numb")
        names.append(arr[1]+" conc")
        values.append(float(arr[8]))
        values.append(float(arr[9]))
        values.append(float(arr[10]))
        i+=3

    return names,values


#################33
# TEMP

def intersection(variantFile):
    #names=["Intersection", "Post", "Het/Hom", "Ti/Tv","known", "novel", "Pre", "Het/Hom", "Ti/Tv","known", "novel" ]
    names=["Total","Het/Hom","nHets","nHomRef","nHomVar","overlHapMap77", "concHapMap77", "overlHapMap78","concHapMap78", "overl1000G78", "conc1000G78", "overldbSNP", "concdbSNP", "Intersection","Het/Hom","nHets","nHomRef","nHomVar","overlHapMap77","concHapMap77","overlHapMap78","concHapMap78", "overl1000G78","conc1000G78","overldbSNP", "concdbSNP","Post","Het/Hom","nHets","nHomRef","nHomVar","overlHapMap77", "concHapMap77","overlHapMap78","concHapMap78","overl1000G78", "conc1000G78", "overldbSNP","concdbSNP","Pre", "Het/Hom","nHets","nHomRef","nHomVar","overlHapMap77","concHapMap77","overlHapMap78","concHapMap78","overl1000G78", "conc1000G78","overldbSNP","concdbSNP"]
    values=[]
    file=open(variantFile).read()
    CO=file.split("CompOverlap :")[1].split("\n")
    CV=file.split("CountVariants :")[1].split("\n")
    #TI=file.split("TiTvVariantEvaluator :")[1].split("\n")
    #print re.split("[ \t]+",CV[1])
    #print re.split("[ \t]+",CV[1])[25]
    #print re.split("[ \t]+",CV[3])[25]
    values.append(int(re.split("[ \t]+",CO[17])[5])) #total 
    values.append(float(re.split("[ \t]+",CV[17])[25])) #het/hom
    values.append(float(re.split("[ \t]+",CV[17])[18])) #nHets
    values.append(float(re.split("[ \t]+",CV[17])[19])) #nHomRef
    values.append(float(re.split("[ \t]+",CV[17])[20])) #nHomVar
    values.append(float(re.split("[ \t]+",CO[17+18])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[17+18])[10])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[17+(18*2)])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[17+(18*2)])[10])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[17])[9])) #1kg
    values.append(float(re.split("[ \t]+",CO[17])[10])) #1kg
    values.append(float(re.split("[ \t]+",CO[17+(18*3)])[9])) #snpdb
    values.append(float(re.split("[ \t]+",CO[17+(18*3)])[10])) #snpdb

    values.append(int(re.split("[ \t]+",CO[8])[5])) #Intersection
    values.append(float(re.split("[ \t]+",CV[8])[25])) #het/hom
    values.append(float(re.split("[ \t]+",CV[8])[18])) #nHets
    values.append(float(re.split("[ \t]+",CV[8])[19])) #nHomRef
    values.append(float(re.split("[ \t]+",CV[8])[20])) #nHomVar
    values.append(float(re.split("[ \t]+",CO[8+18])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[8+18])[10])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[8+(18*2)])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[8+(18*2)])[10])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[8])[9])) #1kg
    values.append(float(re.split("[ \t]+",CO[8])[10])) #1kg
    values.append(float(re.split("[ \t]+",CO[8+(18*3)])[9])) #snpdb  
    values.append(float(re.split("[ \t]+",CO[8+(18*3)])[10])) #snpdb

    values.append(int(re.split("[ \t]+",CO[2])[5])) #Post+filtered inPre
    values[-1]+=(int(re.split("[ \t]+",CO[11])[5])) #Post
    values.append(float(re.split("[ \t]+",CV[2])[25])) #Post+filtered inPre het/hom
    values[-1]+=(float(re.split("[ \t]+",CV[11])[25])) #Post het/hom
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CV[2])[18])) #Post+fiPre nHets
    values[-1]+=(float(re.split("[ \t]+",CV[11])[18])) #Post nHets
    values.append(float(re.split("[ \t]+",CV[2])[19])) #Post+fiPre nHomRef
    values[-1]+=(float(re.split("[ \t]+",CV[11])[19])) #Post nHomRef
    values.append(float(re.split("[ \t]+",CV[2])[20])) #Post+fiPre nHomVar
    values[-1]+=(float(re.split("[ \t]+",CV[11])[20])) #Post nHomVar
    values.append(float(re.split("[ \t]+",CO[2+18])[9])) #1hapmap1
    values[-1]+=(float(re.split("[ \t]+",CO[11+18])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[2+18])[10])) #1hapmap1
    values[-1]+=(float(re.split("[ \t]+",CO[11+18])[10])) #1hapmap1
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[2+(18*2)])[9])) #1hapmap2
    values[-1]+=(float(re.split("[ \t]+",CO[11+(18*2)])[9])) #1hapmap2    
    values.append(float(re.split("[ \t]+",CO[2+(18*2)])[10])) #1hapmap2
    values[-1]+=(float(re.split("[ \t]+",CO[11+(18*2)])[10])) #1hapmap2
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[2])[9])) #1kg
    values[-1]+=(float(re.split("[ \t]+",CO[11])[9])) #1kg
    values.append(float(re.split("[ \t]+",CO[2])[10])) #1kg
    values[-1]+=(float(re.split("[ \t]+",CO[11])[10])) #1kg
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[2+(18*3)])[9])) #snpdb
    values[-1]+=(float(re.split("[ \t]+",CO[11+(18*3)])[9])) #snpdb
    values.append(float(re.split("[ \t]+",CO[2+(18*3)])[10])) #snpdb
    values[-1]+=(float(re.split("[ \t]+",CO[11+(18*3)])[10])) #snpdb
    values[-1]/=2

    values.append(int(re.split("[ \t]+",CO[5])[5])) #Pre+filtered inPost
    values[-1]+=(int(re.split("[ \t]+",CO[14])[5])) #Pre
    values.append(float(re.split("[ \t]+",CV[5])[25])) #Post+filtered inPre het/hom
    values[-1]+=(float(re.split("[ \t]+",CV[14])[25])) #Post het/hom
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CV[5])[18])) #Post+fiPre nHets
    values[-1]+=(float(re.split("[ \t]+",CV[14])[18])) #Post nHets
    values.append(float(re.split("[ \t]+",CV[5])[19])) #Post+fiPre nHomRef
    values[-1]+=(float(re.split("[ \t]+",CV[14])[19])) #Post nHomRef
    values.append(float(re.split("[ \t]+",CV[5])[20])) #Post+fiPre nHomVar
    values[-1]+=(float(re.split("[ \t]+",CV[14])[20])) #Post nHomVar
    values.append(float(re.split("[ \t]+",CO[5+18])[9])) #1hapmap1
    values[-1]+=(float(re.split("[ \t]+",CO[14+18])[9])) #1hapmap1
    values.append(float(re.split("[ \t]+",CO[5+18])[10])) #1hapmap1
    values[-1]+=(float(re.split("[ \t]+",CO[14+18])[10])) #1hapmap1
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[5+(18*2)])[9])) #1hapmap2
    values[-1]+=(float(re.split("[ \t]+",CO[14+(18*2)])[9])) #1hapmap2
    values.append(float(re.split("[ \t]+",CO[5+(18*2)])[10])) #1hapmap2
    values[-1]+=(float(re.split("[ \t]+",CO[14+(18*2)])[10])) #1hapmap2
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[5])[9])) #1kg
    values[-1]+=(float(re.split("[ \t]+",CO[14])[9])) #
    values.append(float(re.split("[ \t]+",CO[5])[10])) #
    values[-1]+=(float(re.split("[ \t]+",CO[14])[10])) #
    values[-1]/=2
    values.append(float(re.split("[ \t]+",CO[5+(18*3)])[9])) #snpdb
    values[-1]+=(float(re.split("[ \t]+",CO[14+(18*3)])[9])) #
    values.append(float(re.split("[ \t]+",CO[5+(18*3)])[10])) #
    values[-1]+=(float(re.split("[ \t]+",CO[14+(18*3)])[10])) #
    values[-1]/=2


    return names,values


##########33
# Temp ende
##########

def coverage(file):
    cont=open(file).read().split("\n")
    names=cont[0].split("\t")[1::]
    values=[]
    for i in cont[1].split("\t")[1::]:
        values.append(float(i))
    #if(printing):
    #    print str(values)+" "+file
    return names,values                    



# adds an array [a3,b3,c3] as a column
# a1, a2, a3
# b1, b2, b3
# c1, c2, c3
def addValues(results,values):
    if(results==[]):
        for v in values:
            results.append([v])
    else:
        for v in range(0,len(values)):
            results[v].append(values[v])
    return results
        

#######3
# MAIN
#######3
oaresult=[]
for d in dir:
    result=[]
    psresult=[]
    name=os.listdir(d)
    name.sort()
    for f in name:
        if (re.compile(ext).search(f)):
#        if(f[-len(ext)::]==ext):
            try:
                if (type=="samstats"):
                    names,values=samstats(d+"/"+f)
                if (type=="samstatsrecal"):
                    names,values=samstatsrecal(d+"/"+f)
                if (type=="bamdistMapped"):
                    names,values=bamDist(d+"/"+f, 5)
                if (type=="coverage"):
                    names,values=coverage(d+"/"+f)                    
                if (type=="variant"):
                    names,values=variant(d+"/"+f)
                if (type=="tophat"):
                    names,values=tophat(d+"/"+f)
                if (type=="times"):
                    names,values=time(d+"/"+f)
                if (type=="target"):
                    names,values=onTarget(d+"/"+f)
                if (type=="intersection"):
                    names,values=intersection(d+"/"+f)     
                result=addValues(result,values)
                filename=f
                if (link):
                    filename="<a href=\""+d.replace("illumina/","")+"/"+f+"\">"+f+"</a>"
                psresult.append([values,filename])
                oaresult=addValues(oaresult,values)
                    
            except :
                sys.stderr.write("error with "+d+"/"+f+"\n")
                traceback.print_exc()
                #sys.exit()
    print "\n#### "+d
    printStats(result,names,psresult)

if (overAll):
    print "\n#### over all"
    print "-----------------------------"
    print "-----------------------------"
    printStats(oaresult,names,0)


#python /clusterdata/hiseq_apps/hiSeqInf/bin/Summary.py Ks50/tophat tph.bam.stats tophat
#python2 /clusterdata/hiseq_apps/hiSeqInf/bin/Summary.py qout/bwa/ .out times