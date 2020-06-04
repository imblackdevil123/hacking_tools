import base64,os
    
 
with open("h.wav","rb") as file:
    d = base64.b64encode(file.read())   
     
with open("h1.wav","wb") as fil:
    fil.write(base64.b64decode(d))  
      