#!/bin/bash

rm -f /home/public/LR_out
while IFS= read -r in; do
    output_str=`lrcalc mult $in`
    max=0
    
    # split between each data chunk (different mu,nu)
    echo "---" >> /home/public/LR_out
    while IFS= read -r out; do
        echo "$out $in" >> /home/public/LR_out
    done <<< "$output_str"
    
done < /home/public/LR_in
