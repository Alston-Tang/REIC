__author__ = 'Tang'

from app import root_path
import magic,os
import json

upload_directory = '/static/upload'
upload_full_dir = (root_path+upload_directory).replace('\\', '/')

def get_file_inf(name,directory,full_dir):
    inf={}
    full_path=full_dir+'/'+name

    inf['name']=name
    inf['type']=magic.from_file(full_path,mime=True)
    inf['size']=os.stat(full_path).st_size
    inf['url']=(directory+'/'+name).replace('/','\\/')
    inf['thumbnailUrl']=inf['url']
    inf['deleteUrl']=inf['url']
    inf['deleteType']='DELETE'
    return inf

class GetHandler:
    def __init__(self, **opt):
        if 'select_dir' in opt:
	    self.directory=upload_directory+'/'+opt['select_dir']
            self.full_dir =upload_full_dir+'/'+opt['select_dir']
        else:
            raise NameError('No specify upload directory')

        # Check End
        self.files = []
        for file in os.listdir(self.full_dir):
	    if not os.path.isfile(self.full_dir+'/'+file):
		raise IOError('File not exists')
	    self.files.append(get_file_inf(file,self.directory,self.full_dir))
            
    def get(self):
        return json.dumps({'files':self.files}).replace('\\\\','\\')
    def post(self):
	pass
	 
    
