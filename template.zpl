^XA

^FX Enable accents etc
^CI0
^FX Set print width
^PW400

^FX This is the first line
^FO20,20
^A@N,30,30,E:ARI003.TTF
^FB350,1,0,L,0
^FD$name1
^FS

^FX This is the second line
^FO20,60
^A@N,30,30,E:ARI003.TTF
^FB350,1,0,L,0
^FD$name2
^FS

^FX This is the horizontal line
^FO10,100
^GB350,2,2,B,0
^FS

^FX This is the date
^FO370,15
^A@B,40,30,E:ARI004.TTF
^FB180,1,0,C,0
^FD$due_date\&
^FS

^FX This is the barcode
^FO40,110
^BY1
^BCN,70,Y,N
^FD$barcode
^FS

^FX This is the print date
^FO10,186
^A@N,5,5,E:ARI003.TTF
^FB150,1,0,L,0
^FDPrinted: $print_date
^FS

^XZ
