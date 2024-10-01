from cgitb import text
from importlib.resources import path
import pandas as pd
import os
import glob
import re
import sys


#get path of python file

path = os.path.dirname(sys.argv[0])
print ("Le path : ",path)

#Get user inputs from input.txt

inputPath = (os.path.join(path,"input.txt")) #paths used in program
tempPath = (os.path.join(path,"TempDocs"))
dir = r"G:\My Drive\WAFERORGANIZATION"

ReadIfWafer = 'Using Wafer Id?:' #Strings to read the lines from the input.txt file
ReadUsingWaferID = 'Wafer to use:'
ReadCartID = 'CartID:'
ReadColour = 'Colour:'
ReadBatch = 'BatchID:'
ReadWafers = 'Wafers to check:'
ReadBinVal = 'BinValue:'
ReadSubBinVal = 'SubBin:'
allLines = ''

InputFile = open(inputPath,'r') #open txt file
Lines = InputFile.readlines()
for i in Lines:
    allLines = allLines + i #Add all lines from txt file to string

WafersToCheck = InputFile.read()
if ReadWafers in allLines: #group up the Wafers to check and place them in seperate temporary file
    print ("Found it")
    wafers = allLines.split(ReadWafers) [1].split('end')[0] # split from reading wafers to the word end at the end of the doc
    text_file = open(os.path.join(tempPath,"JustWafes.txt"), "w") #open a temp doc
    text_file.write(wafers) #write to it
    text_file.close()

###CREATE FUNCTION FOR DIS OR LIST IDK###
for line in Lines: # check for each user input on txt fileand assign them to variable
    if ReadIfWafer in line:
        IfWafer = str(line.split(': ')[1].split('\n')[0])
    if ReadUsingWaferID in line:
        UsingWaferID = str(line.split(': ')[1].split('\n')[0]).casefold()
    if ReadCartID in line:
        LeCartID = str(line.split(': ')[1].split('\n')[0]).casefold()
    # if ReadColour in line:
    #     colour = (line.split(': ')[1].split('\n')[0])
    if ReadBatch in line:
        batch = str(line.split(': ')[1].split('\n')[0]).casefold()
    if ReadBinVal in line:
        BinVal = int(line.split(': ')[1].split('\n')[0])
    if ReadSubBinVal in line:
        SubBinVal = str(line.split(': ')[1].split('\n')[0]).casefold()

# print (IfWafer)
# # print (colour)
# print (batch)
# print (BinVal)
# print (SubBinVal)


if os.path.exists(os.path.join(path,str(BinVal)+"-"+SubBinVal.upper()+"-"+"BinValues.csv")): #check if file already exists and if it does delete it
    os.remove(os.path.join(path,str(BinVal)+"-"+SubBinVal.upper()+"-"+"BinValues.csv"))
    print("file  named with bin vval and sub bin val has been deleted successfully")
else:
    print("The file does not exist!")

if os.path.exists(os.path.join(path,UsingWaferID+"-"+(LeCartID.upper())+"-"+"BinValues.csv")): #check if file already exists and if it does delete it
    os.remove(os.path.join(path,UsingWaferID+"-"+(LeCartID.upper())+"-"+"BinValues.csv"))
    print("file  named with WaferID and CartID has been deleted successfully")
else:
    print("The file does not exist!")

if (IfWafer == 'yes'): #check if the user wishes to use a cartridge ID as a user input
    ReadingWafer=True
    for root, dirs, files in os.walk(dir): #find the csv specified in the input.txt file
        for name in files:
            if name.casefold().startswith(UsingWaferID):
                print (os.path.join(root,name))
                df2 = pd.read_csv(os.path.join(root,name)) #append csv to dataframe
                MisInput=1
    d=0
    while (d< len(df2)): #look for cartridge ID and append its bin and Sub Bin values to Bin Val
        if (df2.iloc[d]['Cartridge ID'].casefold() == LeCartID):
            print ("Found this bithc")
            BinVal = df2.iloc[d]['Bin Number']
            SubBinVal = df2.iloc[d]['Sub Bin']#appending variables
        d = d+1

WAFETextFile = open(os.path.join(tempPath,"JustWafes.txt"), "r")
LeLines = WAFETextFile.readlines()

WaferIDArray = [] #create array to hold the WaferID names
for line in LeLines:
    if (len(line) > 2):
        WaferIDArray.append(line.split('\n')[0]) #appending Wafer ID names

print (WaferIDArray)

Leheaders = 0
MisInput = 0
y=0
print (WaferIDArray)
while y < len(WaferIDArray):
    MisInput = 0 #variable created for error of not finding the file specified in the user Input
    for root, dirs, files in os.walk(dir): # serch through directory and all child directories
        for name in files:
            if name.startswith((WaferIDArray[y])):
                print (os.path.join(root,name))
                df = pd.read_csv(os.path.join(root,name))
                MisInput=1
    # print (df)
# print(df.to_string()) 
#print (df.iloc[26]['WaferID'])
    if(MisInput ==0): #Let the user know if their file was not found
        print("ERROR couldn't find file", (WaferIDArray[y]))

    if (MisInput == 1): #If a file was found create the arrays that will hold the data
        FoundWaferIDS = []
        FoundCartIDS = []
        FoundWavelengths = []
        FoundMinNum = []
        FoundMaxNum = []
        FoundRange = []
        FoundSTDS = []
        FoundBinNumbers = []
        FoundSubBin = []
        FoundAvailability = []

        binnums= []
        subnums= []
        x=0
        size = len(df)
        while (x<size): #append all bin numbers to array
            binnums.append(df.iloc[x]['Bin Number'])
            x = x+1
        #print (binnums)

        z = 0
        while (z<size):#append all sub bin values to array
            subnums.append(df.loc[z]['Sub Bin'])
            z = z+1
        x=0


        ###MAKE FUNCTION FOR APPEND WHERE YOU JUST APPEND EVERYTHING###
        while (x<size):
            if (binnums[x] == BinVal and df.iloc[x]['Availability'] =='Available'): # if the binvalues match and they are available
                FoundWaferIDS.append(df.iloc[x]['WaferID']) #Append each attribute of row of csv
                FoundCartIDS.append(df.iloc[x]['Cartridge ID'])
                FoundWavelengths.append(df.iloc[x]['Wavelength (nm)'])
                FoundMinNum.append(df.iloc[x]['Minumum value'])
                FoundMaxNum.append(df.iloc[x]['Mamimum Value'])
                FoundRange.append(df.iloc[x]['Range (nm)'])
                FoundSTDS.append(df.iloc[x]['Standard Deviation (nm)'])
                FoundBinNumbers.append(df.iloc[x]['Bin Number'])
                FoundSubBin.append(df.iloc[x]['Sub Bin'])
                FoundAvailability.append(df.iloc[x]['Availability'])
                #If statements to add the specified bin values from the other bins closest to bin/sub bin / see drawing for explanation
            if(SubBinVal == 'A'):
                if (binnums[x] == (BinVal-1) and str(subnums[x]) == 'B' and df.iloc[x]['Availability'] =='Available'): # if sub bin is 'a' check for the prior bin sub bin 'b'
                    FoundWaferIDS.append(df.iloc[x]['WaferID']) #Append each attribute of row of csv
                    FoundCartIDS.append(df.iloc[x]['Cartridge ID'])
                    FoundWavelengths.append(df.iloc[x]['Wavelength (nm)'])
                    FoundMinNum.append(df.iloc[x]['Minumum value'])
                    FoundMaxNum.append(df.iloc[x]['Mamimum Value'])
                    FoundRange.append(df.iloc[x]['Range (nm)'])
                    FoundSTDS.append(df.iloc[x]['Standard Deviation (nm)'])
                    FoundBinNumbers.append(df.iloc[x]['Bin Number'])
                    FoundSubBin.append(df.iloc[x]['Sub Bin'])
                    FoundAvailability.append(df.iloc[x]['Availability'])
            if(SubBinVal == 'B'):
                if (binnums[x] == (BinVal+1) and str(subnums[x]) == 'A' and df.iloc[x]['Availability'] =='Available'): # if sub bin is 'b' check for the next bin sub bin 'a'
                    FoundWaferIDS.append(df.iloc[x]['WaferID']) #Append each attribute of row of csv
                    FoundCartIDS.append(df.iloc[x]['Cartridge ID'])
                    FoundWavelengths.append(df.iloc[x]['Wavelength (nm)'])
                    FoundMinNum.append(df.iloc[x]['Minumum value'])
                    FoundMaxNum.append(df.iloc[x]['Mamimum Value'])
                    FoundRange.append(df.iloc[x]['Range (nm)'])
                    FoundSTDS.append(df.iloc[x]['Standard Deviation (nm)'])
                    FoundBinNumbers.append(df.iloc[x]['Bin Number'])
                    FoundSubBin.append(df.iloc[x]['Sub Bin'])
                    FoundAvailability.append(df.iloc[x]['Availability'])
            x = x+1

        #Place data in Dataframe ready to write to CSV
        newdf = pd.DataFrame({ # Columns of csv 
            #                    'Index': LeIndex, # Name of column : array of values
                            'WaferID': FoundWaferIDS,
                            'Wavelength (nm)': FoundWavelengths,
                            'Cartridge ID': FoundCartIDS,
                            'Minumum value': FoundMinNum,
                            'Mamimum Value': FoundMaxNum,
                            'Range (nm)': FoundRange,
                            'Standard Deviation (nm)': FoundSTDS,
                            "Bin Number": FoundBinNumbers, 
                            "Sub Bin": FoundSubBin,
                            "Availability": FoundAvailability
                                        })
        print (newdf)
        
        #Write dataframes to csv

        if (IfWafer == 'yes'):
            if (Leheaders == 0):
                newdf.to_csv(os.path.join(path,UsingWaferID+"-"+(LeCartID.upper())+"-"+"BinValues.csv"), mode='a', index=False, header=True) #write first one with headers
                Leheaders = 1
            else:
                newdf.to_csv(os.path.join(path,UsingWaferID+"-"+(LeCartID.upper())+"-"+"BinValues.csv"), mode='a', index=False, header=False) #Write the rest with no headers
        else:
            if (Leheaders == 0):
                newdf.to_csv(os.path.join(path,str(BinVal)+"-"+SubBinVal.upper()+"-"+"BinValues.csv"), mode='a', index=False, header=True) #write first one with headers
                Leheaders = 1
            else:
                newdf.to_csv(os.path.join(path,str(BinVal)+"-"+SubBinVal.upper()+"-"+"BinValues.csv"), mode='a', index=False, header=False) #Write the rest with no headers

    y = y+1            

