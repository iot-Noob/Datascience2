try:
    import os
    import pytesseract
    from PyPDF2 import PdfReader
    import io
    from PIL import Image
    import matplotlib as plt
    from difflib import SequenceMatcher
    import csv
    from datetime import datetime
except ImportError as e:
    print(f"Error importing a required module: {e}")
    print("Attempting to install missing libraries...")

    try:
        import subprocess
        subprocess.run(["pip", "install", "PyPDF2", "Pillow", "matplotlib","pytesseract"])
        print("Libraries installed successfully.")
    except Exception as install_error:
        print(f"Error installing libraries: {install_error}")
        print("Please install the required libraries manually.")

# Now you can use the libraries


class pdf_handler:
    


    def __init__(self,path):
        self._mdp=None
        self._mbp=None
        self._reader=None
        self.path=path ##path of current dir contain all PDF
        self.cpno=None ## total page no of current pdf
        self.currentPage=None ## current page of PDF
        self.pdfextxt=None ## extracted pdf txt
        self.Fname=None # current File name
        self.Croot=None #Variable for root file path
        self.current_datetime = datetime.now() #get cfurrent date and time
        self.formatted_datetime=self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.cur_img_fo=None## image file object flobal variable extract form PDF
        self._cur_img=None #File obj to image coonverted 
        pass
    #to get all pdf list form dir user define

    def logs(self,txt,filenames):
        try:
            if os.path.exists(f'logs'):
                with open(f'logs/{filenames}.txt','a',encoding='utf-8') as lft:
                    lft.write(txt)
             

            else:
                os.mkdir('logs')
                with open(f'logs/{filenames}.txt','a',encoding='utf-8') as lft:
                    lft.write(txt)


        except FileExistsError as lfne:
            print("log file not Exist ",lfne)

        except FileNotFoundError as lfnf:
            print("log file not foound",lfnf)

        except Exception as le:
            print("log  eerror ",le)

    
 


    def get_all_pdf(self): 
        
        try:
            for root,_,files in os.walk(self.path):
                self.Croot=root
                for f in files:
                    self.Fname=f
                    bp=os.path.join(root,f)
                    if(bp.endswith('.pdf')):
                        dp=os.path.split(bp)
                        self._mdp=dp
                        self._mbp=bp
                        self.ReadPDF()
        except Exception as r:
            print("Error read pdf ,",r)
 
            raise r
 
  

    def ReadPDF(self): ## Open and read entire PDF and scrap images text and also OCR it
        try:
            reader=PdfReader(self._mbp)
            self._reader=reader
            for pno, page in enumerate(reader.pages):
                ##save page no in golbal private variable of class
                self.cpno=pno 
                ##save page in golbal private variable of class
                self.currentPage=page 
                self.scrape_text() ## Scrap txt and save it as txt
                self.Scrap_Images() #scrap images and save it on same dir
                self.OCR_Image_Obj() #OCR extracted miages from PDF at same time
                pass
            
        except Exception as e:
            print("Read PDF error ",e)
            self.logs(f'\n{self.formatted_datetime} Read PDF error {e} from {self._mbp}\n','Errorlogs')
            raise e
  
    def Scrap_Images(self): ##Extract images from every page of PDF
        try:
            self.stip=os.path.join(self.Croot,os.path.splitext(self.Fname)[0]+f"_Page_No_{self.cpno}.png")
            for ifo in self.currentPage.images:
                self.cur_img_fo=ifo
                img=Image.open(io.BytesIO(ifo.data))## Convert image file obj to image
                self._cur_img=img
                img.save(self.stip,quality=42)
                self.logs(f'\n{self.formatted_datetime} {self._mbp} save image  as {self.stip}\n','logs')
                print(f"Save image from base path pdf {self._mbp} image {self.stip} ")
 
      
 
        except Exception as sir:
 

            print("Scrap image from PDF  error ",sir)
            self.logs(f'\n{self.formatted_datetime} Scrape image error form PDF {sir} from {self._mbp}\n','Errorlogs')
            raise sir

        pass

    def scrape_text(self):
        self.extract_text() ## extractt tedxt from current page of PDF
        self.save_txt_file(self.pdfextxt) ##save it as txt file in same folder location

        pass

    def extract_text(self): # extract text form PDF
        try: 
            self.pdfextxt=self.currentPage.extract_text()
            pass
        except FileExistsError as fer:
            self.logs(f'\n{self.formatted_datetime} Extract text error {fer} from {self._mbp}\n','Errorlogs')
            pass
        except FileNotFoundError as fnf:
            self.logs(f'\n{self.formatted_datetime} Extract text error {fnf} from {self._mbp}\n','Errorlogs')
            pass
 
        except Exception as ce:
            print("Scrape text error!! ",ce)
            pass
    def save_txt_file(self,data,cin=None): ## Save thifs as output on same path as txt
        try:
            
            self.stfp=os.path.join(self.Croot,os.path.splitext(self.Fname)[0]+f"{cin} _Page_No_{self.cpno}.txt")
            print(self.stfp)
            with open(self.stfp,'w',encoding='utf-8') as sf:
                sf.write(data)
                print(f"{self.formatted_datetime}  and saved at {self.stfp}")
                self.logs(f'\n{self.formatted_datetime} {self._mbp} save as {self.stfp}\n','logs')

        except Exception as efe:
            self.logs(f'\n{self.formatted_datetime} {self._mbp} derive path = {self.stfp} has error {efe}\n','Errorlogs')
            print("Error save file , ",efe)
 
    def OCR_Image_Obj(self,psm=11,oem=3): ##OCR imageas object from PDF
        try:
            my_config = f"--psm {psm} --oem {oem}"
            txt = pytesseract.image_to_string(self._cur_img, config=my_config,lang='eng')
            self.save_txt_file(txt,'OCR')
      

        except Exception as oce:
            print("OCR Error",oce)
            self.logs(f'\n{self.formatted_datetime} {self._mbp} OCR Error {oce}\n','Errorlogs')
            print("Error save file , ",oce)
            raise oce
        
    def OCR_Image(self,path,psm=11,oem=3): ##OCR imageas  form path
        try:
            my_config = f"--psm {psm} --oem {oem}"
            txt = pytesseract.image_to_string(path, config=my_config,lang='eng')
            self.save_txt_file(txt,'OCR')
      

        except Exception as oce:
            print("OCR Error",oce)
            self.logs(f'\n{self.formatted_datetime} {self._mbp} OCR Error {oce}\n','Errorlogs')
            print("Error save file , ",oce)
            raise oce

class Main(pdf_handler):
    def __init__(self, path):
        super().__init__(path)
 
    pass

    def Pdf_Main(self):
        try:
            self.get_all_pdf()
        except Exception as e:
            print("Some class main error ",e)
    
    def measure_accuracy(self,ocr_value,ground_value): ##meausre and return accuracy from OCR and Ground values
   
        sm = SequenceMatcher(None, ocr_value, ground_value)
        true_positive_char_num = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag== 'equal':
                true_positive_char_num += (j2 - j1)
            else:
                pass
        
        return true_positive_char_num/len(ground_value)
    def save_csv(self,dd,fieldname=[],sdp=None,ofn=None):
        try:
            file_exists = os.path.isfile(f'{sdp}/{ofn}.csv')
            with open(f'{sdp}/{ofn}.csv',mode='a') as ncsv:
                
                writer=csv.DictWriter(ncsv,fieldnames=fieldname)# name of csv and field name to write to tell csv i wsan to write
                if not file_exists or os.stat(f'{sdp}/{ofn}.csv').st_size == 0:
                    writer.writeheader()
                writer.writerow(dd)
        except Exception as e:
            print("Error save CSV ",e)
            self.logs(f'\n{self.formatted_datetime} Save CSV error  {e}\n','Errorlogs')
    
 
if __name__=="__main__":
    cfp=r'PDF'

    try:
        m1=Main(cfp)
        #m1.Pdf_Main()
        #m1.save_csv({"name":"talha","age":28},['name','age'],'.','talha')
    
    except Exception as ef:
        print("Some error occur ",ef)
 