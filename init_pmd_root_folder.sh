#!/bin/sh

module load Python/3.9.5-gimkl-2020a

python init_root_folder_4_sta_code_ana.py -sld libs -slfp pmdrules.xml -eslf -slfrp pmd-bin-* -eslfr -rn pmd -rd ../my_codesnippet_analysis -ucrd -dln libs -an mvn_apps -xn xmlanalysisreports -ecn errorcodeanalysis -ccn completecodeanalysis 