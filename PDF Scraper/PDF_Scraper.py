try:
    import os
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
        subprocess.run(["pip", "install", "PyPDF2", "Pillow", "matplotlib"])
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
        self.Croot=None
        self.current_datetime = datetime.now()
        self.formatted_datetime=self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        self.cur_img_fo=None
 
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
 
  

    def ReadPDF(self): ## Open and read entire PDF
        try:
            reader=PdfReader(self._mbp)
            self._reader=reader
            for pno, page in enumerate(reader.pages):
                ##save page no in golbal private variable of class
                self.cpno=pno 
                ##save page in golbal private variable of class
                self.currentPage=page 
                self.scrape_text()
                self.Scrap_Images()
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
                img=Image.open(io.BytesIO(ifo.data))
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

    def extract_text(self):
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
    def save_txt_file(self,data):
        try:
            
            self.stfp=os.path.join(self.Croot,os.path.splitext(self.Fname)[0]+f"_Page_No_{self.cpno}.txt")
            print(self.stfp)
            with open(self.stfp,'w',encoding='utf-8') as sf:
                sf.write(data)
                print(f"{self.formatted_datetime}  and saved at {self.stfp}")
                self.logs(f'\n{self.formatted_datetime} {self._mbp} save as {self.stfp}\n','logs')

        except Exception as efe:
            self.logs(f'\n{self.formatted_datetime} {self._mbp} derive path = {self.stfp} has error {efe}\n','Errorlogs')
            print("Error save file , ",efe)
 
 

class Main(pdf_handler):
    def __init__(self, path):
        super().__init__(path)
    pass

    def Pdf_Main(self):
        self.get_all_pdf()

        pass
 
cfp=r'PDF'

try:
    m1=Main(cfp)
    m1.Pdf_Main()
except Exception as ef:
    print("Some error occur ",ef)
 
