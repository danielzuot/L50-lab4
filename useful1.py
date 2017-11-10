from useful import np,plt,findall,ceil,floor
import os


def ind_of(value,arr):
    for j in range(len(arr)):
            if (arr[j] == value or j == len(arr)-1):
                return j
            elif (arr[j] > value):
                return j-0.5

def smallest_index(value, arrarr):
    smalls = []
    for i in range(10):
        smalls.append(ind_of(value,arrarr[i]))
    return min(smalls)

def largest_index(value, arrarr):
    larges = []
    for i in range(10):
        larges.append(ind_of(value,arrarr[i]))
    return max(larges)
    
def getrtts(exp,crsid):
    rtts= [[] for i in range(10)]
    for i in range(10):
        with open('./'+crsid+'/pings/'+exp+'_'+str(i)) as f:
            for j in f:
                j = findall(r'time=(.*?) ms',j)[0]
                rtts[i].append(float(j)*1000)
        rtts[i] = sorted(rtts[i])
    return rtts

def getunsortedrtts(exp,crsid):
    rtts= [[] for i in range(10)]
    for i in range(10):
        with open('./'+crsid+'/pings/'+exp+'_'+str(i)) as f:
            for j in f:
                j = findall(r'time=(.*?) ms',j)[0]
                rtts[i].append(float(j)*1000)
    return rtts

def getrttsdroppedfirst(exp, crsid):
    rtts= [[] for i in range(10)]
    for i in range(10):
        with open('./'+crsid+'/pings/'+exp+'_'+str(i)) as f:
            for j in f:
                j = findall(r'time=(.*?) ms',j)[0]
                rtts[i].append(float(j)*1000)
        rtts[i] = sorted(rtts[i])
        del rtts[i][-1]
    return rtts

# you will use functions under this line

def getrtt(ffile,crsid,num):
    rtt= []
    with open('/root/'+crsid+'/L50Lab1/'+ffile) as f:
            for j in range(num):
                rt = f.next()
                rt = findall(r'time=(.*?) ms',rt)[0]
                rtt.append(float(rt)*1000)
    rtt = sorted(rtt)
    return rtt

def graph1(exp,crsid,div,num):
    rtts= getrtts(exp,crsid)
    avgs = []
    for i in range(num):
        avg = np.median([rtts[j][i] for j in range(10)])
        avgs.append(avg)
    values, base = np.histogram(avgs, bins=1000)
    cumulative = np.cumsum(values/float(num))
    plt.plot(base[:-1], cumulative)
    plt.ylabel("Cumulative probability")
    plt.xlabel("RTT (us)")

    minn = int(ceil(avgs[0]/ div)*div)
    maxx = int(floor(avgs[num-1] / div)*div)
    errxs = np.arange(minn,maxx+1,div)
    minsmaxs = [[],[]]
    errys = []
    for i in errxs:
        ind = ind_of(i,avgs)
        errys.append((ind+1)/float(num))
        sml = smallest_index(i, rtts)
        minsmaxs[0].append(abs(ind-sml)/float(num))
        lrg = largest_index(i, rtts)
        minsmaxs[1].append(abs(ind-lrg)/float(num))
    plt.errorbar(errxs, errys, yerr=minsmaxs,linestyle="none")
    plt.show()

def graph2(exp,crsid,div,num):
    rtts = getunsortedrtts(exp, crsid)
    avgs = []
    for i in range(num):
        avg = np.median([rtts[j][i] for j in range(10)])
        avgs.append(avg)
    plt.plot(avgs)
    plt.show()



def graph3(exp,crsid,div,num):
    rtts= getrttsdroppedfirst(exp,crsid)
    avgs = []
    for i in range(num):
        avg = np.median([rtts[j][i] for j in range(10)])
        avgs.append(avg)
    values, base = np.histogram(avgs, bins=1000)
    cumulative = np.cumsum(values/float(num))
    plt.plot(base[:-1], cumulative)
    plt.ylabel("Cumulative probability")
    plt.xlabel("RTT (us)")

    minn = int(ceil(avgs[0]/ div)*div)
    maxx = int(floor(avgs[num-1] / div)*div)
    errxs = np.arange(minn,maxx+1,div)
    minsmaxs = [[],[]]
    errys = []
    for i in errxs:
        ind = ind_of(i,avgs)
        errys.append((ind+1)/float(num))
        sml = smallest_index(i, rtts)
        minsmaxs[0].append(abs(ind-sml)/float(num))
        lrg = largest_index(i, rtts)
        minsmaxs[1].append(abs(ind-lrg)/float(num))
    plt.errorbar(errxs, errys, yerr=minsmaxs,linestyle="none")
    plt.show()

def graph_error(data):
    meds = map(np.median,data)
    mins = map(min,data)
    maxs = map(max,data)
    minsmaxs = [[],[]]
    for i in range(len(data)):
        minsmaxs[0].append(abs(mins[i] - meds[i]))
        minsmaxs[1].append(abs(maxs[i] - meds[i]))
    return meds,minsmaxs