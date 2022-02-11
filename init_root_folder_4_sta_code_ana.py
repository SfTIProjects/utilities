##########################################################################################################
# User Instruction:                                                                                      #
# Download the version of the static code analysis libraries e.g., pmd-bin-x.x.x into the libs folder    #
# Also put the customised or static code analysis checks/rules you want to use into the libs folder      #
#                                                                                                        #
# Script Functionalities:                                                                                #
# 1. main folder e.g pmd, chkstyle, sprtbg                                                               #
# 2. subfolder where all the library files will be kept e.g. libs                                        #
#   2a. libraries into the libs folder e.g.,                                                             #
#       2i.  customised rules xml (pmdrules.xml)                                                         #
#       2ii. pmd downloaded lib for performing the analysis using the command line (pmd-bin-6.39.0)      #
#            Note: if you are using maven you may not need 2ii                                           #
# 3. subfolder where all the mvn apps will be saved e.g. mvn_apps                                        #
# 4. subfolder where all the xml results will be saved e.g. xmlreports                                   #
# 5. subfolder where all the errorneous java codes will be saved e.g. errorcodeanalysis                  #
#    Note: this may not be used for the pmd analysis                                                     #
# 6. subfolder where all the parsed java codes will be saved e.g. completecodeanalysis                   #
#    Note: this may not be used for the pmd analysis                                                     #
#                                                                                                        #
##########################################################################################################

# to run scrit for PMD
# 1st execute this command to make the script runnable
# chmod u+x init_pmd_root_folder.sh
# 2nd run it
# bash init_pmd_root_folder.sh

# Using Common Root Directory #
###############################
# python init_root_folder_4_sta_code_ana.py -sld libs -slfp pmdrules.xml -eslf -slfrp pmd-bin-* -eslfr -rn pmd -rd ../my_codesnippet_analysis -ucrd -dln libs -an mvn_apps -xn xmlreports -ecn errorcodeanalysis -ccn completecodeanalysis

# NOT Using Common Root Directory #
###################################
# python init_root_folder_4_sta_code_ana.py -sld libs -slfp pmdrules.xml -eslf -slfrp pmd-bin-* -eslfr -rn pmd -rd ../my_codesnippet_analysis -dln libs -dld /path/to/make/lib/folder -an mvn_apps -ad /path/to/make/mav_apps/folder -xn xmlreports -xd /path/to/make/xmlreports/folder -ecn errorcodeanalysis -ecd /path/to/make/errorcodeanalysis/folder -ccn completecodeanalysis -ccd /path/to/make/completecodeanalysis/folder



# to run scrit for Checkstyle
# 1st execute this command to make the script runnable
# chmod u+x init_cks_root_folder.sh
# 2nd run it
# bash init_cks_root_folder.sh

# to run scrit for Spotbugs
# 1st execute this command to make the script runnable
# chmod u+x init_stbg_root_folder.sh
# 2nd run it
# bash init_stbg_root_folder.sh






import os

import subprocess as sp

import argparse

parser = argparse.ArgumentParser(
    description='Creates and prepares the root folder for the static code analysis (e.g., PMD, CheckStyle, Spotbugs ).'
)



# e.g1., path/to/where/pmd/checkstyle/spotbugs/rules/xml/files/and/others/can/be/found
# e.g2., libs
parser.add_argument(
    "-sld",
    "--sourcelibdir",
    help="Directory to the library to copy from source to destination library "
)

parser.add_argument(
    "-eslf",
    "--exportsourcefile",
    action="store_true",
    help="Do you need to export a library file"
)

# e.g., pmdrules.xml
parser.add_argument(
    "-slfp",
    "--sourcelibfilepattern",
    default = '',
    help="Pattern for fetching the library file (s) to copy from the source library folder to the destination folder"
)

parser.add_argument(
    "-eslfr",
    "--exportsourcefolder",
    action="store_true",
    help="Do you need to export a library folder"
)

# e.g., pmd-bin-*
parser.add_argument(
    "-slfrp",
    "--sourcelibfolderpattern",
    default = '',
    help="Pattern of the library folder to copy from the source library folder to the destination folder"
)

#e.g. pmd, checkstyle, spotbugs
parser.add_argument(
    "-rn",
    "--rootname",
    help="Name of the root folder for the static code analysis."
)

# e.g. ../my_codesnippet_analysis
parser.add_argument(
    "-rd",
    "--rootdir",
    help="Directory to create the root folder"
)

parser.add_argument(
    "-ucrd",
    "--usecommonrootdir",
    action="store_true",
    help="Use common root directory"
)

# e.g., libs
parser.add_argument(
    "-dln",
    "--destinationlibname",
    help="Name of the destination library folder for the static code analysis."
)

# e.g. ../use/this/if/you/want/libs/in/a/diff/path/from/root
parser.add_argument(
    "-dld",
    "--destinationlibdir",
    help="Directory to create the destination library folder where the checks/rules will be copied to"
)

# e.g., mvn_apps
parser.add_argument(
    "-an",
    "--appname",
    help="Name of the app folder for the static code analysis."
)

# e.g. ../use/this/if/you/want/mvn_app/in/a/diff/path/from/root
parser.add_argument(
    "-ad",
    "--appdir",
    help="Directory to create the app folder where the code snippets files will be saved"
)

# e.g., xmlreports
parser.add_argument(
    "-xn",
    "--xmlname",
    help="Name of the xml static code analysis results folder."
)

# e.g. ../use/this/if/you/want/xmlreports/in/a/diff/path/from/root
parser.add_argument(
    "-xd",
    "--xmldir",
    help="Directory to create the xml folder where the static code analysis xml results will be saved."
)

# e.g., errorcodesnippets
parser.add_argument(
    "-ecn",
    "--errocodename",
    help="Name of the errors for the static code analysis folder."
)

# e.g. ../use/this/if/you/want/errorcodesnippets/in/a/diff/path/from/root
parser.add_argument(
    "-ecd",
    "--errorcodedir",
    help="Directory to create the error folder where the errorneous codes snippets will be saved"
)

# e.g., completecodeanalysis
parser.add_argument(
    "-ccn",
    "--completecodename",
    help="Name of the completeted the static code analysis folder."
)

# e.g. ../use/this/if/you/want/completecodeanalysis/in/a/diff/path/from/root
parser.add_argument(
    "-ccd",
    "--completecodedir",
    help="Directory to create the completed code folder where the completed codes snippets will be saved"
)


args = parser.parse_args()


src_lib_dir = args.sourcelibdir
exp_src_lib_file = args.exportsourcefile
src_lib_file_patt = args.sourcelibfilepattern
exp_src_lib_folder = args.exportsourcefolder
src_folder_patt = args.sourcelibfolderpattern


root_name = args.rootname
root_dir = args.rootdir
use_comm_root_dir = args.usecommonrootdir
dst_lib_name = args.destinationlibname
dst_lib_dir = args.destinationlibdir
app_name = args.appname
app_dir = args.appdir
xml_name = args.xmlname
xml_dir = args.xmldir
erro_code_name = args.errocodename
error_code_dir = args.errorcodedir
complete_code_name  = args.completecodename
complete_code_dir  = args.completecodedir



#1. make the folders
#2. save the required libraries from source to dest

def mk_folders_n_save_req_libs_4m_src_2_dest():
    
   
    root_full_path = '{}/{}'.format(root_dir, root_name)
    dst_lib_full_path = '{}/{}'.format(dst_lib_dir, dst_lib_name)
    app_full_path = '{}/{}'.format(app_dir, app_name)
    xml_full_path = '{}/{}'.format(xml_dir, xml_name)
    erro_code_full_path = '{}/{}'.format(error_code_dir, erro_code_name)
    complete_code_full_path = '{}/{}'.format(complete_code_dir, complete_code_name)
    
    
    if use_comm_root_dir:
        dst_lib_full_path = '{}/{}'.format(root_full_path, dst_lib_name)
        app_full_path = '{}/{}'.format(root_full_path, app_name)
        xml_full_path = '{}/{}'.format(root_full_path, xml_name)
        erro_code_full_path = '{}/{}'.format(root_full_path, erro_code_name)
        complete_code_full_path = '{}/{}'.format(root_full_path, complete_code_name)
       
    #Step1: make folders
    
    #make the root folder
    folder = root_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    #make the destination library folder
    folder = dst_lib_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    
    #make the app folder
    folder = app_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    
    #make the xml reports folder
    folder = xml_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    
    #make the folder for the code analysis error files
    folder = erro_code_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    
    #make the folder code analysis complete files
    folder = complete_code_full_path
    # output: path/to/Post.csv => path/to
    mkdir_cmd = 'mkdir {}'.format(folder)
    cmd = sp.run(
        mkdir_cmd, # command
        capture_output=True,
        text=True,
        shell=True
    )
    
    #Step1: copy the libs file/folder from source lib to dest lib
    if exp_src_lib_file:
        # copy lib files  with this pattern
        cp_cmd = 'cp {}/{} {}'.format(src_lib_dir, src_lib_file_patt, dst_lib_full_path)
        cmd = sp.run(
            cp_cmd, # command
            capture_output=True,
            text=True,
            shell=True
        )
    
    if exp_src_lib_folder:
        # copy lib folders with this pattern
         # copy lib files  with this pattern
        cp_cmd = 'cp -r {}/{} {}'.format(src_lib_dir, src_folder_patt, dst_lib_full_path)
        cmd = sp.run(
            cp_cmd, # command
            capture_output=True,
            text=True,
            shell=True
        )

# invoke the function        
mk_folders_n_save_req_libs_4m_src_2_dest()