# alias
alias ns="nuv saas"
alias nrc="nuv remote client"
alias nrt="nuv remote client task"
alias nrs="nuv remote client shell"

# setvar
A_B64=$(echo hello | base64 -w0)

BIG="$(seq 1 1000v | base64 | fold -w 80)"
BIG_B64=$(echo $BIG | base64 -w0)

nrs dev hostname

nrs dev nuv remote setvar VAR=A VAL_B64=$A_B64
nrs dev -- nuv remote getvar VAR=A

nrs dev nuv remote setvar VAR=BIG VAL_B64=$BIG_B64
nrs dev -- nuv remote getvar VAR=BIG

