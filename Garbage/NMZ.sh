
oTime=3
aTime=2
oWait=$oTime
aWait=$aTime
oTimeOff=1
oTimeOff=2
oNum=40
aNum=64
finished='FALSE'
o=0
a=0
start=$(date +%s)
xyRange=12
doAb=0

###invintory###
#  0  1  2  3 #
#  4  5  6  7 #
#  8  9 10 11 #
# 12 13 14 15 #
# 16 17 18 19 #
# 20 21 22 23 #
# 24 25 26 27 #
###############

# Usage:    overload
# Clicks slot for overload potion
# and keeps track of how many doses
# have been taken.
overload() {
    echo '-----begin overload-----'
    let 'dose=(40-oNum)'
    let 'slot=(dose/4)'
    let 'row=(slot/4)'
    let 'column=(slot%4)'
    xdif=$RANDOM
    ydif=$RANDOM
    let 'xdif%=xyRange'
    let 'ydif%=xyRange'
    let 'x=(column*42)+933+xdif-(xyRange/2)'
    let 'y=(row*36)+490+ydif-(xyRange/2)'
    echo 'dose='$dose
    echo 'slot='$slot
    echo 'row='$row
    echo 'column='$column
    echo 'x='$x
    echo 'y='$y
    xdotool mousemove $x $y click 1
    echo '------end overload-----'
    sleep 3
}

# Usage:    absorbtion
# Clicks slot for absorbtion potion
# and keeps track of how many doses
# have been taken.
absorbtion() {
    if [[ $doAb == 1 ]] ; then
        echo '-----begin absorbtion-----'
        let 'dose=(64-aNum)'
        let 'slot=(dose/4)+12'
        let 'row=(slot/4)'
        let 'column=(slot%4)'
        xdif=$RANDOM
        ydif=$RANDOM
        let 'xdif%=xyRange'
        let 'ydif%=xyRange'
        let 'x=(column*42)+933+xdif-(xyRange/2)'
        let 'y=(row*36)+490+ydif-(xyRange/2)'
        echo 'dose='$dose
        echo 'slot='$slot
        echo 'row='$row
        echo 'column='$column
        echo 'x='$x
        echo 'y='$y
        xdotool mousemove $x $y #click 1
        echo '-----end absorbtion------'
    else
        let 'doAb = 1'
    fi
    sleep 3
}

while [[ $aNum -gt 0 || $oNum -gt 0 ]] ; do
    cur=$(date +%s)
    dif=$((cur-start))
    
    #if time to overload
    if [[ $(( dif >= oTime )) && $o == 0 && $oNum > 0 ]] ; then
        overload
        ((oNum--))
        let 'o = 1'
        oTimeOff=$RANDOM
        let 'oTimeOff%=3'
        let 'oTime=oWait+oTimeOff'
    elif [[ $((dif%oTime)) != 0 && $o == 1 ]] ; then
        let 'o = 0'
    fi

    #if time for absorbtion
    if [[ $(( dif >= aTime )) && $a == 0 && $aNum > 0 ]] ; then
        absorbtion
        ((aNum--))
        let 'a = 1'
        aTimeOff=$RANDOM
        let 'aTimeOff%=3'
        let 'aTime=aWait+aTimeOff'
    elif [[ $((dif%aTime)) != 0 && $a == 1 ]] ; then
        let 'a = 0'
    fi

    #if time for pray flick
done

