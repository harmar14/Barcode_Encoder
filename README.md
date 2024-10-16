# Barcode_Encoder
Here is my implementation of the Code128 algorithm and this is how the code works.  
**Input**
```
python code128.py 5891
```
**Output**
```
ÍZ{DÎ
```
And some more examples:
```
6453 -> Í`UeÎ
5956 -> Í[XfÎ
5547 -> ÍWOPÎ
1234567 -> Í,BXÈ7LÎ
```
**To turn the output into a normal barcode, you need to apply the Code128 font to it**  
A few words about the algorithm: https://en.wikipedia.org/wiki/Code_128  
The website I used to check results: https://www.bcgen.com/fontencoder
