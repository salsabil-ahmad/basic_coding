from django.shortcuts import render
import cx_Oracle
import configparser
from django.contrib.auth import views as auth_views
from django.http import HttpResponse,HttpResponseRedirect
from .filehandle import readcsv
from django.http import JsonResponse


config = configparser.RawConfigParser()
config.read('C:/Users/salsabil.ahmad/Desktop/connection.properties')
uimusername = config.get('UIMDatabase', 'username');
print(uimusername)
uimpassword = config.get('UIMDatabase', 'password');
uimdbdetails = config.get('UIMDatabase', 'dbconnection');
osmusername = config.get('OSMDatabase', 'username');
print(osmusername)
osmpassword = config.get('OSMDatabase', 'password');
osmdbdetails = config.get('OSMDatabase', 'dbconnection');



def index(request):
#     if request.user.is_authenticated():
    if "GET" == request.method:
        return render(request, 'dbpagesal/dbcon.html', {})
    else:
        fro= [request.POST.get('fromdate')]
        print(fro)
        to= [request.POST.get('todate')]
        print(to)
        sqlquery="SELECT ENTITYID FROM UIM.SERVICE WHERE SPECIFICATION= '27150055' AND ADMINSTATE='IN_SERVICE' AND CREATEDDATE BETWEEN '%s' and '%s'"%(fro[0], to[0])
        print(sqlquery)
        con = cx_Oracle.connect(uimusername+'/'+uimpassword+'@'+uimdbdetails)
        cur = con.cursor()
        cur.execute("SELECT ENTITYID FROM UIM.SERVICE WHERE SPECIFICATION= '27150055' AND ADMINSTATE='IN_SERVICE' AND CREATEDDATE BETWEEN '%s' and '%s'"%(fro[0], to[0]))
        res = cur.fetchall() 
        cur.close()
        #print (res)
        find=[]
        mylist=[]
        coun=[]
        #success=[]
        count=0
        for i in res:
            count=count+1
            cur=con.cursor()
            #sql="SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(i[0],i[0])
            #print(sql)
            #print(i[0])
            cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(i[0],i[0]))
            fe = cur.fetchall()
            cur.execute("SELECT ENTITYID FROM UIM.SERVICEASSIGNMENT where SERVICECONSUMER in '%s'"%i[0])
            re = cur.fetchall()
            # print(res)
            voice=[]
            wifi=[]
            out='Success'
            for j in re:
                cur.execute("SELECT ENTITYID,ID, NAME FROM UIM.SERVICE WHERE CURRENTASSIGNMENT in '%s'"%j[0])
                fet=cur.fetchall()
                # print(fet)
                cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(fet[0][0],fet[0][0]))
                got=cur.fetchall()
                # print(got)
               
                print(fet[0][2])
                if "Mobile_Account_RFS" in fet[0][2]:
                    cur.execute("SELECT DISTINCT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in (%s,%s)) AND VALUE not in ('Value Not Set','Not Available')"%(fe[0][0],got[0][0]))
                    ans=cur.fetchall()
                    out=readcsv(ans,"Mobile_Account_RFS")
                    # print(ans)
                    print(out)
                    #return render(request, 'dbpagesal/respage.html', {'result':ans})
                elif "WIFI_Access_RFS" in fet[0][2]:
                    cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                    wifi=cur.fetchall()
                    out=readcsv(wifi,"WIFI_Access_RFS")
                    # print(wifi)
                    print(out)
                    #return render(request, 'dbpagesal/respage.html', {'resultw':wifi})
                elif "Voicemail_Service_RFS" in fet[0][2]:
                    cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                    voice=cur.fetchall()
                    out=readcsv(voice,"Voicemail_Service_RFS")
                    # print(voice)
                    print(out)
                    #return render(request, 'dbpagesal/respage.html', {'resultv':voice})
                #print(fet[0][0])
         
            # sql = "SELECT UIM.SERVICE.ID as Service_ID, UIM.BUSINESSINTERACTION.EXTERNALNAME as Order_ID, UIM.SERVICE.ADMINSTATE as Status FROM UIM.SERVICE CROSS JOIN UIM.BUSINESSINTERACTION WHERE  UIM.SERVICE.ENTITYID='%s' and UIM.BUSINESSINTERACTION.ENTITYID in(SELECT BUSINESSINTERACTION FROM UIM.BUSINESSINTERACTIONITEM where TOENTITYREF='%s')"%(i[0],fet[0][0])
            #print(sql)
            cur.execute("SELECT UIM.SERVICE.ENTITYID as ENTITYID, UIM.SERVICE.ID as Service_ID, UIM.BUSINESSINTERACTION.EXTERNALNAME as Order_ID,UIM.SERVICE.ADMINSTATE as Status FROM UIM.SERVICE CROSS JOIN UIM.BUSINESSINTERACTION WHERE UIM.SERVICE.ENTITYID='%s' and UIM.BUSINESSINTERACTION.ENTITYID in (SELECT BUSINESSINTERACTION FROM UIM.BUSINESSINTERACTIONITEM where TOENTITYREF='%s' AND ENTITYCLASS='BusinessInteractionItemDAO')"%(i[0],fe[0][0]))
            find = cur.fetchall()
            if str(out)=='Success':
                find.append('PASSED')
            else:
                find.append('FAILED')
            # find.append(success)
            print(find)
            mylist.append(find)
            print(mylist)
        coun.append(count)   
        return render(request, 'dbpagesal/dbcon.html', {'result':mylist,'coin':count,'fromd':fro,'tod':to})
        cur.close()
        con.close()   
      
def verify(request):
    if "GET" == request.method:
        return render(request, 'dbpagesal/respage.html', {})
        # return render(request, 'dbpagesal/orderpage.html', {})
    else:
        id= request.POST.get('name')
        print(id)
        con = cx_Oracle.connect(uimusername+'/'+uimpassword+'@'+uimdbdetails)
        cur = con.cursor()
        cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(id,id))
        re=cur.fetchall()
        cur.execute("SELECT ENTITYID FROM UIM.SERVICEASSIGNMENT where SERVICECONSUMER in '%s'"%id)
        res = cur.fetchall()
        print(res)
        voice=[]
        wifi=[]
        ans=[]
        for i in res:
            cur.execute("SELECT ENTITYID,ID, NAME FROM UIM.SERVICE WHERE CURRENTASSIGNMENT in '%s'"%i[0])
            fet=cur.fetchall()
            print(fet)
            cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(fet[0][0],fet[0][0]))
            got=cur.fetchall()
            print(got)
            print(fet[0][2])
            if "Mobile_Account_RFS" in fet[0][2]:
                cur.execute("SELECT DISTINCT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in (%s,%s)) AND VALUE not in ('Value Not Set','Not Available') order by NAME"%(re[0][0],got[0][0]))
                ans=cur.fetchall()
                print(ans)
                #return render(request, 'dbpagesal/respage.html', {'result':ans})
            elif "WIFI_Access_RFS" in fet[0][2]:
                cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                wifi=cur.fetchall()
                print(wifi)
                #return render(request, 'dbpagesal/respage.html', {'resultw':wifi})
            elif "Voicemail_Service_RFS" in fet[0][2]:
                cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                voice=cur.fetchall()
                print(voice)
                #return render(request, 'dbpagesal/respage.html', {'resultv':voice})
        return render(request, 'dbpagesal/respage.html', {'resultm':ans,'resultw':wifi,'resultv':voice})
        cur.close()
        con.close()

def info(request):
    if "GET" == request.method:
        return render(request, 'dbpagesal/orderpage.html', {})
    else:
        Oid= request.POST.get('Order')
        print(Oid)
        con = cx_Oracle.connect(osmusername+'/'+osmpassword+'@'+osmdbdetails)
        cur=con.cursor()
        q="SELECT order_seq_id as Order ID,ORD_TXN_REASON as Order Status FROM OM_ORDER_HEADER where REFERENCE_NUMBER='%s'"%Oid
        print(q)
        cur.execute("SELECT order_seq_id as OrderID,ORD_TXN_REASON as Order_Status,REFERENCE_NUMBER FROM OM_ORDER_HEADER where REFERENCE_NUMBER='%s'"%Oid)
        global RESULT1
        RESULT1=cur.fetchall()
        print(RESULT1)
        return render(request, 'dbpagesal/orderpage.html',{'output':RESULT1})

def detail(request):
    if "GET" == request.method:
        return render(request, 'dbpagesal/orderpage.html', {})
    else:
        Oid= request.POST.get('orderid')
        con = cx_Oracle.connect('ordermgmt/passw0rd@tr001buosm-db.ddc.teliasonera.net:1521/TRBUOSM')
        cur=con.cursor()
        mylist=[]
        all=[]
        cur.execute("select ORDER_SEQ_ID from OM_ORDER_AMENDMENT_KEY where key='<ID>%s</ID>'"%Oid)
        res=cur.fetchall()
        mylist.append(res[0][0])
        cur.execute("SELECT ORDER_SEQ_ID FROM OM_ORDER_HEADER where REFERENCE_NUMBER in('%s')"%Oid)
        re=cur.fetchall()
        print(re)
        for i in re:
            mylist.append(re[0][0])
            q="SELECT ORDER_SEQ_ID,ORD_TXN_REASON FROM OM_ORDER_HEADER where REFERENCE_NUMBER in('%s-tom')"%i
            print(q)
            cur.execute("SELECT ORDER_SEQ_ID FROM OM_ORDER_HEADER where REFERENCE_NUMBER in('%s-tom')"%i)
            r=cur.fetchall()
            mylist.append(r[0][0])
            print(r)
        print(mylist)
        for i in mylist:
            cur.execute("SELECT H.ORDER_SEQ_ID as Order_ID,T.TASK_MNEMONIC as TASK_NAME,S.STATE_MNEMONIC as TASK_STATUS FROM OM_ORDER_HEADER A,OM_HIST$ORDER_HEADER H, OM_TASK T,OM_STATE S WHERE A.ORDER_SEQ_ID=H.ORDER_SEQ_ID AND H.TASK_ID= T.TASK_ID AND S.STATE_ID=H.HIST_ORDER_STATE_ID AND T.TASK_TYPE in('A','M') and A.ORDER_SEQ_ID in ('%s') AND H.hist_seq_id in(SELECT max(hist_seq_id) FROM OM_HIST$ORDER_HEADER where ORDER_SEQ_ID in('%s'))"%(i,i))
            out=cur.fetchall()
            all.append(out)
        print(all)
        return render(request, 'dbpagesal/orderpage.html',{'output1':all,'output':RESULT1})

def complete(request):
    if "GET" == request.method:
        return render(request, 'dbpagesal/newpage.html', {})
    else:
        Oid= request.POST.get('orderid')
        print(Oid)
        con = cx_Oracle.connect(uimusername+'/'+uimpassword+'@'+uimdbdetails)
        cur=con.cursor()
        cur.execute("SELECT SERVICE as Service_Entity_ID FROM SERVICECONFIGURATIONVERSION where ENTITYID in (SELECT ENTITYID FROM BUSINESSINTERACTION WHERE ID in(SELECT PARTICIPATINGENTITYID FROM BUSINESSINTERACTIONITEM WHERE BUSINESSINTERACTION in (SELECT ENTITYID FROM BUSINESSINTERACTION WHERE EXTERNALNAME='%s')))"%Oid)
        rem=cur.fetchall()
        print(rem)
        res=[]
        for i in rem:
            res.append(i[0])
        find=[]
        mylist=[]
        coun=[]
        #success=[]
        count=0
        for i in res:
            count=count+1
            cur=con.cursor()
            #sql="SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(i[0],i[0])
            #print(sql)
            print(i)
            cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(i,i))
            fe = cur.fetchall()
            cur.execute("SELECT ENTITYID FROM UIM.SERVICEASSIGNMENT where SERVICECONSUMER in '%s'"%i)
            re = cur.fetchall()
            # print(res)
            voice=[]
            wifi=[]
            out='Success'
            for j in re:
                cur.execute("SELECT ENTITYID,ID, NAME FROM UIM.SERVICE WHERE CURRENTASSIGNMENT in '%s'"%j[0])
                fet=cur.fetchall()
                # print(fet)
                cur.execute("SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONVERSION WHERE SERVICE in '%s' AND VERSIONNUMBER=(SELECT MAX(VERSIONNUMBER) FROM UIM.SERVICECONFIGURATIONVERSION where SERVICE in '%s')"%(fet[0][0],fet[0][0]))
                got=cur.fetchall()
                # print(got)
               
                print(fet[0][2])
                if "Mobile_Account_RFS" in fet[0][2]:
                    cur.execute("SELECT DISTINCT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in (%s,%s)) AND VALUE not in ('Value Not Set','Not Available')"%(fe[0][0],got[0][0]))
                    ans=cur.fetchall()
                    out=readcsv(ans,"Mobile_Account_RFS")
                    # print(ans)
                    print(out)
                    #return render(request, 'dbpage/respage.html', {'result':ans})
                elif "WIFI_Access_RFS" in fet[0][2]:
                    cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                    wifi=cur.fetchall()
                    out=readcsv(wifi,"WIFI_Access_RFS")
                    # print(wifi)
                    print(out)
                    #return render(request, 'dbpage/respage.html', {'resultw':wifi})
                elif "Voicemail_Service_RFS" in fet[0][2]:
                    cur.execute("SELECT NAME, VALUE FROM UIM.SERVICECONFIGITEM_CHAR WHERE CHAROWNER in (SELECT ENTITYID FROM UIM.SERVICECONFIGURATIONITEM where NAME='Properties' AND CONFIGURATION in '%s') AND VALUE not in ('Value Not Set','Not Available')"%got[0][0])
                    voice=cur.fetchall()
                    out=readcsv(voice,"Voicemail_Service_RFS")
                    # print(voice)
                    print(out)
                    #return render(request, 'dbpage/respage.html', {'resultv':voice})
                #print(fet[0][0])
         
            # sql = "SELECT UIM.SERVICE.ID as Service_ID, UIM.BUSINESSINTERACTION.EXTERNALNAME as Order_ID, UIM.SERVICE.ADMINSTATE as Status FROM UIM.SERVICE CROSS JOIN UIM.BUSINESSINTERACTION WHERE  UIM.SERVICE.ENTITYID='%s' and UIM.BUSINESSINTERACTION.ENTITYID in(SELECT BUSINESSINTERACTION FROM UIM.BUSINESSINTERACTIONITEM where TOENTITYREF='%s')"%(i[0],fet[0][0])
            #print(sql)
            cur.execute("SELECT UIM.SERVICE.ENTITYID as ENTITYID, UIM.SERVICE.ID as Service_ID, UIM.BUSINESSINTERACTION.EXTERNALNAME as Order_ID,UIM.SERVICE.ADMINSTATE as Status FROM UIM.SERVICE CROSS JOIN UIM.BUSINESSINTERACTION WHERE UIM.SERVICE.ENTITYID='%s' and UIM.BUSINESSINTERACTION.ENTITYID in (SELECT BUSINESSINTERACTION FROM UIM.BUSINESSINTERACTIONITEM where TOENTITYREF='%s' AND ENTITYCLASS='BusinessInteractionItemDAO')"%(i,fe[0][0]))
            find = cur.fetchall()
            if str(out)=='Success':
                find.append('PASSED')
            else:
                find.append('FAILED')
            #find.append(success)
            print(find)
            mylist.append(find)
            print(mylist)
        coun.append(count)   
        return render(request, 'dbpagesal/newpage.html', {'result':mylist})
        cur.close()
        con.close()
        
        
        
