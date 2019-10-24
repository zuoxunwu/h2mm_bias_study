input1="file1.txt"
declare -a myarray
let i=0
while IFS="," read f1 f2; do
    echo "$f2"
    myarray[i]="$f2"
    ((++i))
done < "$input1"

echo ${myarray[0]}
