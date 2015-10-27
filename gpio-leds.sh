cd /sys/class/gpio

echo 17 > export
echo 27 > export
echo 22 > export
echo 18 > export
echo 23 > export

echo out  > gpio17/direction
echo out  > gpio27/direction
echo out  > gpio22/direction
echo out  > gpio18/direction
echo out  > gpio23/direction

echo 0 > gpio17/value
echo 0 > gpio27/value
echo 0 > gpio22/value
echo 0 > gpio18/value
echo 0 > gpio23/value

echo 1 > gpio17/value
sleep 1
echo 0 > gpio17/value
sleep 1

echo 1 > gpio27/value
sleep 1
echo 0 > gpio27/value
sleep 1

echo 1 > gpio22/value
sleep 1
echo 0 > gpio22/value
sleep 1

echo 1 > gpio18/value
sleep 1
echo 0 > gpio18/value
sleep 1

echo 1 > gpio23/value
sleep 1
echo 0 > gpio23/value
sleep 1


