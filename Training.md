# Details of the training process for the Cascade Classifier in OpenCV

[Details of the OpenCV code development](https://www.element14.com/community/people/Workshopshed/blog/2016/05/20/dragonboard-410c-opencv)

The training application is very hungry for memory and used about 2.5GB on my system. It ran one of my CPUs at between 50% and 100%.

Conveniently the training application tells you how long it runs for, so on my first pass it tool 13 minutes for stage one and finished in about half an hour

Here's the output from the second run where I had a lot more images and set the false alarm rate much lower.

```
opencv_traincascade.exe -data Cascade -vec Dragons.vec -bg Negative.info -numPos 90 -numNeg 2078 -maxFalseAlarmRate 0.05 -numStages 5 -w 50 -h 50 -mode ALL
PARAMETERS:
cascadeDirName: Cascade
vecFileName: Dragons.vec
bgFileName: Negative.info
numPos: 90
numNeg: 2078
numStages: 5
precalcValBufSize[Mb] : 1024
precalcIdxBufSize[Mb] : 1024
acceptanceRatioBreakValue : -1
stageType: BOOST
featureType: HAAR
sampleWidth: 50
sampleHeight: 50
boostType: GAB
minHitRate: 0.995
maxFalseAlarmRate: 0.05
weightTrimRate: 0.95
maxDepth: 1
maxWeakCount: 100
mode: ALL

===== TRAINING 0-stage =====
<BEGIN
POS count : consumed   90 : 90
NEG count : acceptanceRatio    2078 : 1
Precalculation time: 11.939
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1| 0.298845|
+----+---------+---------+
|   4|        1| 0.326275|
+----+---------+---------+
|   5|        1| 0.100096|
+----+---------+---------+
|   6|        1|0.0375361|
+----+---------+---------+
END>
Training until now has taken 0 days 1 hours 53 minutes 16 seconds.

===== TRAINING 1-stage =====
<BEGIN
POS count : consumed   90 : 90
NEG count : acceptanceRatio    2078 : 0.0275363
Precalculation time: 14.096
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1| 0.679018|
+----+---------+---------+
|   4|        1| 0.416747|
+----+---------+---------+
|   5|        1| 0.227623|
+----+---------+---------+
|   6|        1| 0.102021|
+----+---------+---------+
|   7|        1| 0.159769|
+----+---------+---------+
|   8|        1|0.0866218|
+----+---------+---------+
|   9|        1| 0.045717|
+----+---------+---------+
END>
Training until now has taken 0 days 4 hours 26 minutes 52 seconds.

===== TRAINING 2-stage =====
<BEGIN
POS count : consumed   90 : 90
Premature end of JPEG file
NEG count : acceptanceRatio    2078 : 0.00243268
Precalculation time: 13.822
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1|        1|
+----+---------+---------+
|   4|        1| 0.629451|
+----+---------+---------+
|   5|        1|  0.39846|
+----+---------+---------+
|   6|        1| 0.145332|
+----+---------+---------+
|   7|        1|0.0904716|
+----+---------+---------+
|   8|        1|0.0495669|
+----+---------+---------+
END>
Training until now has taken 0 days 6 hours 44 minutes 9 seconds.

===== TRAINING 3-stage =====
<BEGIN
POS count : consumed   90 : 90
Premature end of JPEG file
NEG count : acceptanceRatio    2078 : 0.000160029
Precalculation time: 12.939
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1| 0.558229|
+----+---------+---------+
|   4|        1| 0.762271|
+----+---------+---------+
|   5|        1| 0.508181|
+----+---------+---------+
|   6|        1| 0.374398|
+----+---------+---------+
|   7|        1| 0.290664|
+----+---------+---------+
|   8|        1| 0.192974|
+----+---------+---------+
|   9|        1| 0.188643|
+----+---------+---------+
|  10|        1|  0.12897|
+----+---------+---------+
|  11|        1|0.0914341|
+----+---------+---------+
|  12|        1| 0.104909|
+----+---------+---------+
|  13|        1|0.0418672|
+----+---------+---------+
END>
Training until now has taken 0 days 10 hours 0 minutes 37 seconds.

===== TRAINING 4-stage =====
<BEGIN
POS count : consumed   90 : 90
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
Premature end of JPEG file
NEG count : acceptanceRatio    2078 : 9.49071e-06
Precalculation time: 12.259
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1|        1|
+----+---------+---------+
|   4|        1| 0.770452|
+----+---------+---------+
|   5|        1| 0.591915|
+----+---------+---------+
|   6|        1| 0.421078|
+----+---------+---------+
|   7|        1| 0.381136|
+----+---------+---------+
|   8|        1| 0.275265|
+----+---------+---------+
|   9|        1|   0.1564|
+----+---------+---------+
|  10|        1| 0.128489|
+----+---------+---------+
|  11|        1| 0.149182|
+----+---------+---------+
|  12|        1| 0.114052|
+----+---------+---------+
|  13|        1|0.0524543|
+----+---------+---------+
|  14|        1|0.0822907|
+----+---------+---------+
|  15|        1|0.0548604|
+----+---------+---------+
|  16|        1|0.0202117|
+----+---------+---------+
END>
Training until now has taken 0 days 14 hours 45 minutes 51 seconds.
```
