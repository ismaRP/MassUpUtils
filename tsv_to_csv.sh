#!/bin/bash


OPTIND=1

TEMP=`getopt -o i:o:t: --long input:,output:,tabtocsv: -- "$@"`
eval set -- "$TEMP"

# extract options and their arguments into variables.
reverse=false
while true ; do
    case "$1" in
        -i|--input)
            case "$2" in
                "") echo "Provide input folder" ; exit 1 ;;
                *) inputDir=$2 ; shift 2 ;;
            esac ;;
        -o|--output)
            case "$2" in
                "") echo "Provide destination" ; exit 1 ;;
                 *) outputDir=$2 ; shift 2 ;;
            esac ;;
        -t|--tabtocsv)
            case "$2" in
                ""|true)
                    echo "Transforming tsv to csv"
                    reverse=false ; shift 2 ;;
                "reverse")
                    echo "Transforming csv to tsv"
                    reverse=true ; shift 2 ;;
            esac ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done


echo "Input files in $inputDir"
echo "Output to $outputDir"
echo "Reverse=$reverse"

if [ "$reverse" = true ]; then
  for f in $inputDir/* ; do
    of="$(echo $f | cut -d "/" -f3)"
    cat $f | cut -d "," -f1 | paste - <(cat $f | cut -d "," -f2) > "$outputDir/$of"
    rename 's/\.(csv)/\.tsv/' "$outputDir/$of"
  done
else
  for f in $inputDir/* ; do
    of="$(echo $f | cut -d "/" -f3)"
    cat $f | cut -f1 | paste -d "," - <(cat $f | cut -f2) > "$outputDir/$of"
    rename 's/\.(txt|tsv)/\.csv/' "$outputDir/$of"
  done
fi
