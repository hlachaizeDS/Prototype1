import datetime
import shutil
import os
import openpyxl

#from cycles import dispTime25_nuc,dispTime25_enzyme,dispDBTime,dispBBTime

def readExpID():
    path="ExpID.txt"
    file=open(path,"r")
    number=file.readline()
    file.close()
    file=open(path,"w")
    file.write(str(int(number)+1))
    file.close()
    return number


def saveQuartetControlFile(title,code=""):

    now=datetime.datetime.now()

    #original Quartet file
    original_path=r'D:\Proto7\Quartet_Control.xlsm'
    expID=readExpID()

    #new folder path
    general_path = "C:\\Users\\SynthesisDNASCRIPT\\DNA Script\\SO - Synthesis Operations - Bibliothèque\\S.3 - Proto\\P7\\Quartets"
    folder_path=str(now.year)[2:]+ force2digits(now.month)

    # new file path
    personal_folder_path = str(now.year)[2:] + force2digits(now.month) + force2digits(now.day) + '_P7_' + title + '_' + expID
    file_path = str(now.year)[2:] + force2digits(now.month) + force2digits(now.day) + "_P7_" + title + "_" + expID

    #the quartet control will be copied both in its own folder AND in all folder
    os.makedirs(general_path + '\\' + folder_path, exist_ok=True)
    os.makedirs(general_path + '\\' + folder_path + '\\' + personal_folder_path, exist_ok=True)
    os.makedirs(general_path + '\\' + folder_path +'\\All', exist_ok=True)


    #Copy the Quartet Control file
    final_personal_path=general_path + '\\' + folder_path + '\\' + personal_folder_path + "\\" + file_path + '.xlsm'
    final_all_path=general_path + '\\' + folder_path + '\\All\\' + file_path + '.xlsm'
    shutil.copy(original_path, final_personal_path)
    shutil.copy(original_path, final_all_path)

    # Eventually copy source code
    final_personal_code_path = general_path + '\\' + folder_path + '\\' + personal_folder_path + "\\" + file_path + "_code.txt"
    if code != "":
        code_file = open(final_personal_code_path, "w")
        code_file.write(code)
        code_file.close()

def force2digits(number):
    if number<10:
        return '0'+str(number)
    else:
        return str(number)

if __name__ == "__main__":
    # On crée la racine de notre interface
    saveQuartetControlFile("test")
    #readExpID()