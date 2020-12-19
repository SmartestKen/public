cd /home/k5shao/non-empty
rm -rf /home/k5shao/non-empty/*
mkdir 12513251251
mkdir 12432523521
mkdir 12412351325
mkdir 25325151351
mkdir 43215543212


shopt -s nullglob
for file in /home/k5shao/empty/*/
do
    echo $file
    file="${file%/}"
    echo "${file##*/}"

done 


for file in /home/public/*
do
    echo $file
done



while read -r line; do
    # will lose characters without double quotes
    case "$line" in @*)
        siteFilter=$siteFilter$'\n'$line
    esac
done < "/home/public/test.txt"
echo "$siteFilter"



a=()
a[12357]=12357
a[11111]=11119
a[10101]=10101
a[19565]=19565
a[65466]=65466
for i in ${!a[@]}
do
    echo $i
done

last_check_date=-1
time=(`date +"%s %w %m/%d/%Y"`)
cur_time=${time[0]}
cur_day=${time[1]}
cur_date=${time[2]}

# dequeue part
if [ $cur_date != $last_check_date ]
then
    threshold_pt=`date +%s --date="$cur_date 8:00"`
    before_threshold_allow_time=`date +%s --date="$cur_date-1day 00:00"`
    after_threshold_allow_time=`date +%s --date="$cur_date 00:00"`
    last_check_date=$cur_date
fi

if [[ $cur_time -ge $threshold_pt ]]
then
    allow_time=$after_threshold_allow_time
else
    allow_time=$before_threshold_allow_time
fi


echo "$before_threshold_allow_time $after_threshold_allow_time"



tokens=(0:00 8:00 ?2:00)
if [[ "${tokens[1]}" =~ ^[0-2]?[0-9]:[0-5][0-9]$ && "${tokens[2]}" =~ ^[0-2]?[0-9]:[0-5][0-9]$ ]]
then
    echo "I am here ${tokens[1]} ${tokens[2]}"
fi

cur_day=1
case "123" in $cur_day*)
    echo "I pass switch"
esac
case "231" in $cur_day*)
    echo "I pass switch again"
esac




for file in /home/public/123_construction/*
do
    echo $file
done



for i in {0..30..1}
do
    haha=$((i%10))
    if [[ $haha = 0 ]]
    then
        echo haha
    else
        echo $i
    fi
done
