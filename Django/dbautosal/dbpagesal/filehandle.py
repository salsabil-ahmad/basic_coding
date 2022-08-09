import csv


def readcsv(listfromdb, type):
     with open('C:/Users/salsabil.ahmad/Desktop/csvTestFile.txt', mode='r') as csv_file:
         try:
            #  print(type)
             csv_reader = csv.DictReader(csv_file)
             line_count = 0
             mylist = list()
    #         listfinal - Storing parameters from Query
             listfinal = list()
             serviceType = ""
    #          adding item from db list
             for row in listfromdb:
                listfinal.append(row[0]);
                if row[0] == "ServiceType":
                   serviceType = row[1]    
#              print("Final List: ", listfinal)  
            #  print("SErviceType: ",serviceType)
             for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                if type in row["Account"]:
                #    print(f'\t{row["Account"]}, {row["ServiceType"]} , {row["Parameter"]}, {row["Value"]}.')
                     if serviceType == row["ServiceType"]:
#                        print("checkk",row["Parameter"])
#                    if serviceType in row["ServiceType"]:
#                          print(f'\t{row["Parameter"]}')
                         mylist.append(row["Parameter"])
                line_count += 1
            #  print(f'Processed {line_count} lines.')
#              print(mylist)
             val = "Validated"
             
             if all(item in listfinal for item in mylist):
                 # print('Validated')
                 return "Success"
             else:
                 # print("Validation Failed")
                 missingval = set(mylist).difference(listfinal)
#                  for i in missingval:
#                     print("missing values: ", i)
                 return "Failure"
#                  temp3 =[item not in mylist for item in attr]
#                  print("Missing Attrib:", temp3)
         except FileNotFoundError as fnf_error:
             print(fnf_error)
         except IOError as IO_error:
             print(IO_error)
#        except:
#            print('An error occured.')
         finally:
             mylist.clear()
             csv_file.close()
