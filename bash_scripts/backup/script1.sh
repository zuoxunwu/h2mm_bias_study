input="file1.txt"
# Set "," as the field separator using $IFS 
# and read line by line using while read combo 
while IFS="," read f1 f2; do
# space is need for [ ]
    
    [[ "$f1" = "#".* ]] && continue
    if [ "$f1" = "model" ]; then
        echo "the $f1 is $f2"
    fi
    if [ "$f1" = "datafile" ]; then
        echo "the $f1 is $f2"
    fi
done < "$input"
