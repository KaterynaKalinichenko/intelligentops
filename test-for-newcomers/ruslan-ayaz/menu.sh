#!/bin/bash
echo Create new t2.micro instance.

count=0;

while [ $count -lt 1 ]
do

read -p "Choose an Amazon Machine Image (AMI) for region US West (Oregon), us-west-2:
1. Amazon Linux 2 AMI (HVM), SSD Volume Type
2. Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type
3. Red Hat Enterprise Linux 7.6 (HVM), SSD Volume Type
4. Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
5. Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
6. Or select one of your own AMIs

Press Q to quit.

Select: " AMI
 
	case $AMI in
"1")
bash run-instance.sh ami-032509850cf9ee54e
count=1
;;
"2")
bash run-instance.sh ami-01e24be29428c15b2
count=1
;;
"3")
bash run-instance.sh ami-036affea69a1101c9
count=1
;;
"4")
bash run-instance.sh ami-0bbe6b35405ecebdb
count=1
;;
"5")
bash run-instance.sh ami-076e276d85f524150
count=1
;;
"6")
read -p "Write your own AMI: " oAMI
bash run-instance.sh $oAMI
count=1
;;
"Q" | "q")
exit 0;
;;
*) echo "Invalid option, choose again...
";;

esac
done
