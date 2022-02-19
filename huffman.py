#huffman
import heapq
import os

class BinaryTree:
    def __init__(self,value,frequency):
        self.value=value
        self.frequency=frequency
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.frequency < other.frequency

    def __eq__(self,other):
        return self.frequency == other.frequency



class huffman:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reverseCode={}


    def __frequency(self,text):
        d = {}
        for i in text:
            if i not in d:
                d[i] = 0
            d[i] += 1
        return d

    def __buildHeap(self,frequency_dict):
        for key in frequency_dict:
            frequency=frequency_dict[key]
            binary_Tree_Node=BinaryTree(key,frequency)
            heapq.heappush(self.__heap,binary_Tree_Node)


    def __binaryTree(self):
        while len(self.__heap)>1:
            binary1=heapq.heappop(self.__heap)
            binary2=heapq.heappop(self.__heap)
            freq_sum=binary1.frequency+binary2.frequency
            newNode=BinaryTree(None,freq_sum)
            newNode.left=binary1
            newNode.right=binary2
            heapq.heappush(self.__heap,newNode)
        return


    def __buildCodeHelper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__codes[root.value]=curr_bits
            self.__reverseCode[curr_bits]=root.value
            return


        self.__buildCodeHelper(root.left,curr_bits+ "0" )
        self.__buildCodeHelper(root.right,curr_bits + "1")



    def __buildCode(self):
        root=heapq.heappop(self.__heap)
        self.__buildCodeHelper(root,"")

    def __getEncodedText(self,text):
        encoded_text=""
        for char in text:
            encoded_text+=self.__codes[char]
        return encoded_text

    def __getPaddingEncodedText(self,encoded_text):
        padded_amount=8-(len(encoded_text)%8)
        for i in range(padded_amount):
            encoded_text+="0"
        padded_info="{0:08b}".format(padded_amount)
        padded_Encoded_Text=padded_info+encoded_text
        return padded_Encoded_Text


    def __getBytesArray(self,padded_encoded_text):
        array=[]
        for i in range(0,len(padded_encoded_text),8):
            bytes=padded_encoded_text[i:i+8]
            array.append(int(bytes,2))
        return array



    def compress(self):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+".bin"
        with open(path, 'r+') as file , open(output_path, 'wb') as output:
            text=file.read()
            text=text.rsplit()
            frequency_dict=self.__frequency(text)
            self.__buildHeap(frequency_dict)
            self.__binaryTree()
            self.__buildCode()
            encoded_text=self.__getEncodedText(text)
            padded_encoded_text=self.__getPaddingEncodedText(encoded_text)
            bytes_array=self.__getBytesArray(padded_encoded_text)
            final_bytes=bytes(bytes_array)
            output.write(final_bytes)
        print("compressed")
        return output_path

    def __removePadding(self,text):
        padded_info=text[:8]
        extra_padding=int(padded_info,2)
        text=text[8:]
        text_after_padding=text[:-1*extra_padding]
        return text_after_padding

    def __decodedText(self,text):
        decoded_text=""
        curr_bits=""
        for bits in text:
            curr_bits += bits
            if curr_bits in self.__reverseCode:
                char=self.__reverseCode[curr_bits]
                decoded_text+=char
                curr_bits=""
        return decoded_text




    def decompress(self,input_text):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+"_decompress"+".txt"
        with open(input_text, 'rb') as file, open(output_path,'w') as output:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)
            actual_padding=self.__removePadding(bit_string)
            decoded_text=self.__decodedText(actual_padding)
            output.write(decoded_text)


path='C:/Users/ACER/Desktop/n/sample3.txt'
h=huffman(path)
output_path=h.compress()
h.decompress(output_path)















