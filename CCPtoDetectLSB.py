import cv2
import numpy as np 
import string
import secrets
def msg_to_bin(msg):  
    if type(msg) == str:  
        return ''.join([format(ord(i), "08b") for i in msg])  
    elif type(msg) == bytes or type(msg) == np.ndarray:  
        return [format(i, "08b") for i in msg]  
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:  
        raise TypeError("Input type not supported")  
def hide_data(img, secret_msg):  
    # calculating the maximum bytes for encoding  
    nBytes = img.shape[0] * img.shape[1] * 3 // 8  
    print("Maximum Bytes for encoding:", nBytes)  
    # checking whether the number of bytes for encoding is less  
    # than the maximum bytes in the image  
    if len(secret_msg) > nBytes:  
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")  
    secret_msg += '#####'       # we can utilize any string as the delimiter  
    dataIndex = 0  
    # converting the input data to binary format using the msg_to_bin() function  
    bin_secret_msg = msg_to_bin(secret_msg)  
  
    # finding the length of data that requires to be hidden  
    dataLen = len(bin_secret_msg)  
    for values in img:  
        for pixels in values:  
            # converting RGB values to binary format  
            r, g, b = msg_to_bin(pixels)  
            # modifying the LSB only if there is data remaining to store  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Red pixel  
                pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Green pixel  
                pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            if dataIndex < dataLen:  
                # hiding the data into LSB of Blue pixel  
                pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)  
                dataIndex += 1  
            # if data is encoded, break out the loop  
            if dataIndex >= dataLen:  
                break  
      
    return img  
def encodeText(srcimg,newimg):  
    img = cv2.imread(srcimg)
    s=img.size
    length_data=int(s*0.2)
    data=''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length_data))         
    encodedImage = hide_data(img, data)  
    cv2.imwrite(newimg, encodedImage)  
def calculate_close_unique(src):
    image  = cv2.imread(src)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    n = img.shape[0] #height
    m = img.shape[1] #width
    R =  img[:, :, 0] #RED
    G =  img[:, :, 1]   #GREEN
    B =  img[:, :, 2]   #BLUE
    ccp = 0
    for i in range(0,n):
        for j in range(0,m):
            if( i< n-1 and j < m-1):
                    if abs(int(R[i][j]) - int(R[i+1][j+1]) ) == 1 and abs(int(G[i][j]) - int(G[i+1][j+1]) ) == 1 and abs(int(B[i][j]) - int(B[i+1][j+1]) ) == 1:
                        ccp = ccp + 1
                        
    print(ccp)
    ucp=0
    for i in range(0,n):
        for j in range(0,m):
            if( i< n-1 and j < m-1):
                    if abs(int(R[i][j]) - int(R[i+1][j+1]) ) == 1 or abs(int(G[i][j]) - int(G[i+1][j+1]) ) == 1 or abs(int(B[i][j]) - int(B[i+1][j+1]) ) == 1:
                        ucp = ucp + 1
    print(ucp)
    z1=ccp/ucp
    print("Ti le mau gan nhau tren mau dac biet la",z1)
    return z1
def check():
    img_name = input("Enter image name need detect (with extension): ") 
    img_name_tmp=img_name+"1.png"
    encodeText(img_name,img_name_tmp)
    a=calculate_close_unique(img_name)
    b=calculate_close_unique(img_name_tmp)
    if (a/b)<1:
        print("Stegano Image")
    else:
        print("Cover Image")
check()


