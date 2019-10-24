
declare -a fruit=("banana" "apple" "tomato")

for f1 in "${fruit[@]}"
do
    for f2 in "${fruit[@]}"
    do
    echo ${f1}, ${f2}
    done
done



