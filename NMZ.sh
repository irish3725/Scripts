#TODO:
# variable assignment   x
# while loop            x
# variable reference    x
# get time              x 
# if statement          x
# function declaration  x
# function use          x
# arithmatic            x
# float usage

# Usage:    overload
# Clicks slot for overload potion
# and keeps track of how many doses
# have been taken.
overload() {
    let 'dose=(40-oNum)'
    let 'slot=(dose/4)'
    let 'row=(slot/4)'
    let 'column=(slot%4)'
    echo 'dose='$dose
    echo 'slot='$slot
    echo 'row='$row
    echo 'column='$column
    echo 'inside overload'
}

# Usage:    absorbtion
# Clicks slot for absorbtion potion
# and keeps track of how many doses
# have been taken.
absorbtion() {
    echo 'inside absorbtion'
}

# Usage:    clickSlot

oTime=5
aTime=3
oNum=40
aNum=8
finished='FALSE'
o=0
a=0
start=$(date +%s)

while [[ $aNum -gt 0 || $oNum -gt 0 ]] ; do
    cur=$(date +%s)
    dif=$((cur-start))
    
    #if time to overload
    if [[ $((dif%oTime)) == 0 && $o == 0 && $oNum > 0 ]] ; then
        overload
        ((oNum--))
        echo 'oNum='$oNum
        let 'o = 1'
    elif [[ $((dif%oTime)) != 0 && $o == 1 ]] ; then
        let 'o = 0'
    fi

    #if time for absorbtion
    if [[ $((dif%aTime)) == 0 && $a == 0 && $aNum > 0 ]] ; then
        absorbtion
        ((aNum--))
        echo 'aNum='$aNum
        let 'a = 1'
    elif [[ $((dif%aTime)) != 0 && $a == 1 ]] ; then
        let 'a = 0'
    fi
done

