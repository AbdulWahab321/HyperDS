VERSION = "1.0.3"
    
import io
import pickle
import os
import re
import pyzipper
import shutil
from ast import literal_eval
from abc import ABC
from .exceptions import invalidDataType,syntax_error,InvalidDataType
from .utils import TraceDict,TraceList,search_and_replace
import importlib,textwrap,typing
import os,tempfile
if os.name == "nt":
    try:
        import colorama
        colorama.init()
    except:
        colorama = None
else:
    colorama = 1
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),".config")) as vers:
    VERSION = vers.read().split("=")[1].split('"',maxsplit=1)[1].split('"')[0]
DEFAULT_HDS_CODE_WITHOUT_DEVLOGS = "# File created by HyperDataStorage\n# Editing files manually can create errors!\n# Formating the file can also create errors!\n# Edit files manually at your own risk!"
DEFAULT_HDS_CODE_WITH_DEVLOGS = "# File created by HyperDataStorage\n# Editing files manually can create errors!\n# Formating the file can also create errors!\n# Edit files manually at your own risk!\n\ndevlogs False"
class TargetClass(ABC):   
    def __init__(self,cls):
        self.cls = cls
class _File():
    def __init__(self):
        pass

class HDSIo():
    def __init__(self,path):
        self.path = path
    def read(self,*args, **kwargs):
        pass
    def write(self,*args, **kwargs):
        pass
    def files(self,*args, **kwargs):
        pass
    def close(self,*args, **kwargs):
        pass
class ZipFile(pyzipper.AESZipFile):
    def __init__(self, file, mode = "r", compression = 0, allowZip64 = True, compresslevel = None, *, strict_timestamps: bool = True) -> None:
        super().__init__(file, mode, compression, allowZip64, compresslevel, strict_timestamps=strict_timestamps)
        self.allowZip64 = allowZip64
        self.__path = file
        self.strict_timestamps = strict_timestamps
    def edit(self,file,mode="w"):
        files = []
        for f in self.namelist():
            if f!=file:
                files.append([f,self.read(f)])
        __zf = pyzipper.AESZipFile(self.__path, "w", self.compression, self.allowZip64, self.compresslevel, strict_timestamps=self.strict_timestamps)
        for file_ in files:
            __zf.writestr(file_[0],file_[1])
        file_desc = __zf.open(file,mode)
        ol_wr = file_desc.write
        file_desc.write = lambda data:ol_wr(data.encode() if hasattr(data, 'encode') else data)
        return file_desc
class HDSArchive(HDSIo):
    def __init__(self,path,pwd=None,*zipfile_args,**zipfile_kwargs):
        super().__init__(path)
        self.zipfile_args = zipfile_args
        self.zipfile_kwargs = zipfile_kwargs
        self.archive = True
        self.zipf = (self.path,"r",zipfile_args,zipfile_kwargs)
        self.pwd = pwd
        self.encryption_kwargs = {"encryption":pyzipper.WZ_AES, "nbits":128}
        self.encryption_args = []
        self.file_dt = {}
        if self.pwd:self.pwd = pwd.encode()
        if not os.path.exists(path):
            with ZipFile(self.zipf[0],"w",*self.zipf[2],**self.zipf[3]) as zipf:
                if self.pwd:
                    zipf.setpassword(self.pwd)
                    zipf.setencryption(**self.encryption_kwargs)
                zipf.writestr("main.hds",DEFAULT_HDS_CODE_WITH_DEVLOGS)
        else:
            with ZipFile(self.zipf[0],"a",*self.zipf[2],**self.zipf[3]) as zipf:
                if self.pwd:
                    zipf.setpassword(self.pwd)
                    zipf.setencryption(**self.encryption_kwargs)
                if "main.hds" not in zipf.namelist():
                    zipf.writestr("main.hds",DEFAULT_HDS_CODE_WITH_DEVLOGS)
                else:
                    if "devlogs" not in zipf.read("main.hds").decode("utf-8"):
                        f = zipf.edit("main.hds")
                        exi_dt = zipf.read("main.hds")
                        f.write(DEFAULT_HDS_CODE_WITH_DEVLOGS.encode()+"\n"+exi_dt)
                        f.close()
        with pyzipper.AESZipFile(self.zipf[0],"r",*self.zipf[2],**self.zipf[3]) as zipf:
            if self.pwd:zipf.setpassword(self.pwd)
            for file_ in zipf.namelist():
                self.file_dt[file_] = zipf.read(file_,self.pwd)
        self.temp_files = [] 
    def set_pwd(self,pwd):
        self.pwd = pwd
    def read(self,file,mode="rb",*args):
        data = self.file_dt[file]
        if not mode.endswith("b"):return data.decode() if hasattr(data, "decode") else data
        else:return data.encode() if hasattr(data, "encode") else data
    def write(self,file,data,mode="wb",*args):
        if not mode.endswith("b"):data = data.decode() if hasattr(data, "decode") else data
        else:data = data.encode() if hasattr(data, "encode") else data        
        self.file_dt[file] = data
    def files(self):
        return list(self.file_dt.keys())
    def setencryption(self,**kwargs):
        self.encryption_kwargs.update(kwargs)
    def close(self,close_tempfolder=True):
        with pyzipper.AESZipFile(self.zipf[0],"w",*self.zipf[2],**self.zipf[3]) as zipf:
            if self.pwd:
                
                zipf.setpassword(self.pwd)
                zipf.setencryption(**self.encryption_kwargs)
            for f,d in self.file_dt.items():

                zipf.writestr(f,d)
            zipf.setpassword(self.pwd)

class HDSFolder(HDSIo):
    def __init__(self,path,create_file_if_need=True):
        super().__init__(path)
        self.create_file_if_need = create_file_if_need
        self.archive = True
        if create_file_if_need:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                with open(os.path.join(self.path,"main.hds"),"w") as f:
                    f.write(DEFAULT_HDS_CODE_WITH_DEVLOGS)
            elif not os.path.exists(os.path.join(self.path,"main.hds")):
                with open(os.path.join(self.path,"main.hds"),"w") as f:
                    f.write(DEFAULT_HDS_CODE_WITH_DEVLOGS)
        else:
            raise IOError("No such file or directory: "+path)          
    def read(self,file,mode="r"):
        with open(os.path.join(self.path,file),mode) as f:
            if mode=="rb":return f.read()
            else:return f.read().encode()
    def write(self,file,data,mode="w"):
        with open(os.path.join(self.path,file),mode) as f:
            f.write(data)
    def files(self):
        return os.listdir(self.path)
    def close(self,*args,**kwargs):
        pass

def get_var_format(line):
    format_ = None
    if re.match(r'^.*=\s*".*"', line):
        format_ = "string"
    elif re.match(r'^\s*.*=\s*{.*}', line):
        format_ = "dict"    
    elif re.match(r'^.*=\s*\[\s*.*\s*\]', line):
        format_ = "list"      
    elif re.match(r'^.*=\s*?[0-9]+\s*[\+\-\*\/\/]\s*[0-9]+\s*$', line):
        format_ = "mathematical_expression"
    elif re.match(r'^.*=\s*?\(\s*?.*?\s*?\)\s*?', line):
        format_ = "tuple"   
    elif re.match(r'.*=\s*(true|false|True|False)\s*', line):
        format_ = "boolean"          
    elif re.match(r'.*=\s*(None)\s*', line):
        format_ = "NoneType"      
    elif re.match(r'^.*=\s*\d+\s*$', line):
        format_ = "integer"                         
    elif re.match(r'^.*=\s*\w+\s*?', line):
        format_ = "variable"  
    elif re.match(r"^\s*\d+\.\d+\s*$", line):
        format_ = "float"
    return format_


class Logger():
    def __init__(self,logs,file):
        self.logs = logs
        self.file = file
    def vlog(self,variable,format,value,linenum,line=None,in_=None):
        if self.logs:
            log = f"""
        
    [{self.file}] Parsing variable: {variable} {'in '+in_ if in_ else ''}      
                    type: {format}
                    value: {value}
                    line: {linenum}
                    code: {line}"""
            print(log)
    def baselog(self,data):
        if self.logs:
            if "\n" in data:
                data = f"\n[{self.file}]".join(data)
            else:
                data = f"\n[{self.file}]"+data    
def var_parsed_data(line,parser,file,line_num,format):
    variable = line.split("=")[0].strip()
    if format == "string":
        value = line.split("=")[1].split('"')[1].replace('"',"")
    elif format == "mathematical_expression":
        value = eval(line.split("=")[1])    
    elif format == "dict":
        lines_dict_present = line.split("=")[1]
        value = data_type_parser(lines_dict_present)   
    elif format == 'list':
        value = data_type_parser(line.split("=")[1])      
    elif format == "tuple":
        value = data_type_parser(line.split("=")[1])    
    elif format == "integer":
        value = int(line.split("=")[1])
    elif format == "float":
        value = float(line.split("=")[1])        
    elif format == "variable":
        if variable not in parser.variables[file.split(".hds")[0]]:
            raise InvalidDataType("Variable not defined: "+line.split("=")[1].strip()+" at "+str(line_num+1)+":"+str(line.index(line.split("=")[1][0])+1))        
        value = parser.variables[file.split(".hds")[0]][line.split("=")[1].strip()]
    elif format == "boolean":
        value = bool(line.split("=")[1])
    elif format == "NoneType":
        value = None  
    else:
        raise InvalidDataType("Invalid value: "+line.split("=")[1].strip()+" at "+str(line_num+1)+":"+str(line.index(line.split("=")[1][0]+1)))        
    return variable,[value,format,line_num]
def parse_variable(parser,line,lines,format,target_class,file,line_num):
    data = var_parsed_data(line,parser,file,line_num,format)
    variable = data[0]
    value,format,line_num = data[1]
    
    parser.set_variable(variable,value,file=file.split(".hds")[0])
    #parser.variables[file.split(".hds")[0]][variable] = [value,format,line_num]
    if target_class:setattr(getattr(target_class,file.split(".hds")[0]),variable,value)         
    return variable,value,format
def data_type_parser(line):
    new_line = line
    for idx,i in enumerate(line):
        if i.strip() == "":
            new_line = new_line[idx+1:]
        else:
            break 
    return literal_eval(new_line)
def indentation_parser(lines,ml_idx):
    indentation_count = 0
    total_str = ""
    for character in lines[ml_idx+1]:
        if character == " ":
            indentation_count+=1
        else:
            break    
    for line_num,line in enumerate(lines[ml_idx+1:]):
        if line.startswith(" "*indentation_count):
            total_str+=line[indentation_count:]+"\n"
        elif line.startswith(" "):
            syntax_error("Indentation error at "+str(ml_idx+line_num+2)+":"+str(line.index(line.strip()[0]))) 
        else:
            break
    return total_str,indentation_count  
"""def py_evaluator(matched_line,lines,file_glob,hds,line_num,parse_data):


    ml_idx = lines.index(matched_line)
    eval_lines_str,_ = indentation_parser(lines,ml_idx)
    eval_lines_str = textwrap.indent(eval_lines_str,"")
    exec(eval_lines_str,file_glob)
    return eval_lines_str
"""

def object_initializer(lines,matched_line,file,target_class=None,parser=None):
    ml_idx = lines.index(matched_line)

    obj_name = lines[ml_idx].split(":")[0]
    variables_lines,indentation_count = indentation_parser(lines,ml_idx)
    parser.logger.baselog("Creating object: "+obj_name.strip())
    class _Class():
        def __init__(self):
            pass
    t_cls = _Class()
    for line_num,line in enumerate(variables_lines.split("\n")):
        if line.strip()!="":
            if not re.match(r"([\w]*[\d]*)\s*:\s*",line):
                class __TempParser():
                    def __init__(self):
                        self.logs = False
                data = var_parsed_data(line,__TempParser(),file,ml_idx+line_num+2,get_var_format(line))
                variable = data[0]
                value,format,line_num = data[1]    
                parser.logger.vlog(variable,format,value,ml_idx+line_num+2,line,obj_name.strip())
                setattr(t_cls,variable.strip(),value)
            else:
                name,obj = object_initializer(lines,lines[ml_idx+line_num+1],file,target_class,parser)
                parser.logger.baselog("Creating object: "+name+" inside "+obj_name.strip())
                setattr(t_cls,name.strip(),obj)
    
    return obj_name.strip(),t_cls        
class FileDescriptorStr(io.StringIO):
    def __init__(self,filename,hdsobject:typing.Union[HDSArchive,HDSFolder],file_idx=None,files=[],parser=None):
        self.hdsobject = hdsobject
        self.filename = filename
        self.fi = file_idx
        self.files = files
        self.parser = parser
    def read(self):
        return self.hdsobject.read(self.filename,"rb").decode("utf-8")
    def write(self,__s: str,/):        
        self.hdsobject.write(self.filename,__s,"w")
        if self.fi:
            self.parser.files[self.fi] = [self.filename,__s]
class FileDescriptorByte(io.BytesIO):
    def __init__(self,filename,hdsobject:typing.Union[HDSArchive,HDSFolder],file_idx=None,files=[],parser=None):
        self.hdsobject = hdsobject
        self.filename = filename
        self.fi = file_idx
        self.files = files     
        self.parser = parser   
    def read(self):
        return self.hdsobject.read(self.filename,"rb")    
    def write(self,__b: bytes,/):
        self.hdsobject.write(self.filename,__b,"wb")
        if self.fi:
            self.parser.files[self.fi] = [self.filename,__b]   
class HDSObject():
    def __init__(self,name,inherits=[]):
        self.name = name
        self.inherits = [[name,self]]
        self.inherits.extend(inherits)
        self.variables = {}
        self.code = ""
    def add_var(self,var,value):
        data_type = type(value).__name__
        if isinstance(value, TraceDict):
            value.on_change = lambda ndict: self.add_var(var, ndict)
        elif isinstance(value, TraceList):
            value.callback = lambda nlist: self.add_var(var, nlist)
        elif value is None:
            data_type = "NoneType"
        elif data_type not in ["str", "int", "float", "bool", "tuple", "list", "dict"]:
            invalidDataType(value)
        new_value = f'"{value}"' if data_type == "str" else str(value)
        self.variables[var] = [new_value,data_type]
        self.code+=f"\n{var} = {new_value}"
    def add_obj(self,name):
        inherits = self.inherits.copy()
        return HDSObject(name.strip(),inherits)
    def _finalize(self):
        final_string = ""
        indentations = 0
        clss = 0
        for inherit,cls in reversed(self.inherits):
            final_string+="\n"+" "*4*clss+f"{inherit}:"
            final_string+=' '*4*(clss+1)
            final_string+=("\n"+' '*4*(clss+1)).join(cls.code.split("\n"))+f"\n{' '*4*(clss+1)}"
            indentations+=4
            clss+=1
        return final_string,indentations
class HyperDataStorage():
    def __init__(self,serializer_module=pickle,serializer_dump_args=[pickle.HIGHEST_PROTOCOL],serializer_dump_kwargs={},serializer_load_args=[],serializer_load_kwargs={}):
        self.variables = {"main":{}}
        self.temp_vars = {"main":{}}
        self.python_objs = {"main":{}}
        self.read_python_objs = {"main":{}}
        self.compressed_files = {"main":{}}
        self.pyevals = {"main":[]}
        self.imports = {"hdsimports":{"main":[]},"pyimports":{"main":[]}}
        self.files = [["main.hds",None]]
        self.file_globals = {"main":{}}
        self.hds_codes = {"main":DEFAULT_HDS_CODE_WITHOUT_DEVLOGS}
        self.var_idxs = {"main":{}}
        self.objects = {"main":[]}
        self.parsed_objs = {"main":{}}
        self.logs = True
        self.archive_path = None
        self.new_data = ""
        self.hdsobject:typing.Union[HDSArchive,HDSFolder] = None
        self.serializer_module = serializer_module
        self.serializer_dump_args = serializer_dump_args
        self.serializer_dump_kwargs = serializer_dump_kwargs
        self.serializer_load_args = serializer_load_args        
        self.serializer_load_kwargs = serializer_load_kwargs        
    def new_target_class(self):
        return _new_target_class()
    def read(self,hdsobject,add_python_objs_to_variables=False,target_class=None,allow_pyevals=True,eval_kwargs={}):
        self.hdsobject = hdsobject
        
        if hdsobject.archive:
            self.path = hdsobject.path
            self.data = hdsobject.read("main.hds").decode("utf-8").split("\n")
            self.custom_parse(add_python_objs_to_variables,target_class,self.path,hdsobject,allow_pyevals,eval_kwargs)
        else:
            self.path = hdsobject.path
            self.custom_parse(add_python_objs_to_variables,target_class,hdsobject.path,allow_pyevals=allow_pyevals,eval_kwargs=eval_kwargs)
    def iter_vars(self,file="main"):

        return dict(map(lambda kv:(kv[0],kv[1][0]),list(self.variables[file].copy().items())))
    def add_file(self,filename,data=None):
        self.files.append([filename,data])
        if filename not in self.hdsobject.files():
            self.hdsobject.write(filename,str(data))
        if filename.endswith(".hds"):self.init_file(filename)
    def file_exists(self, filename):
        return filename in self.hdsobject.files()
    def open_file(self,filename,mode="rb"):
        file_idx = None
        files = list(map(lambda x:x[0],self.files.copy()))
        if filename not in files:
            self.add_file(filename," ")
            if "b" in mode:return FileDescriptorByte(filename,self.hdsobject,file_idx,self.files,self)
            else:return FileDescriptorStr(filename,self.hdsobject,file_idx,self.files,self)             
        tfiles = list(filter(lambda x:x[0] == filename,self.files))
        file_idx = self.files.index(tfiles[0])
        if "b" in mode:return FileDescriptorByte(filename,self.hdsobject,file_idx,self.files,self)
        else:return FileDescriptorStr(filename,self.hdsobject,file_idx,self.files,self)            
    def hdsimport(self,current_file,import_filename,zipf,archive=True):

        if import_filename.split(".hds")[0] in self.variables:

            self.variables[current_file].update(self.variables[import_filename.split(".hds")[0]])
            self.read_python_objs[current_file].update(self.read_python_objs[import_filename.split(".hds")[0]])
        elif import_filename in self.hdsobject.files():

            self.init_file(import_filename)
            data = self.hdsobject.read(import_filename).decode("utf-8").split("\n")
            self.custom_parse_one_file(import_filename,data,self.archive_path,None,zipf=zipf)
            self.variables[current_file].update(self.variables[import_filename.split(".hds")[0]])
            self.read_python_objs[current_file].update(self.read_python_objs[import_filename.split(".hds")[0]])             
    def pyimport(self,current_file,python_module):
        module = importlib.import_module(python_module,python_module)
        ## CLASSES ARE NOT SUPPORTED FIX itwhen hds.save
        self.pyimport_variables[current_file.split(".hds")[0]] = vars(module)
    def delete_variable(self, variable, file="main"):
        if variable in self.var_idxs:
            new_code = self.hds_codes.split("\n")
            new_code.pop(self.var_idxs[file][variable])
            self.hds_codes[file] = "\n".join(new_code)
            self.var_idxs[file].pop(variable)
        self.variables[file].pop(variable)

    """
    def whole_str(self):
        str_ = ""
        for line in self.data:
            str_ += line
        return str_
    """
    def get_obj(self,name,file="main"):
        if file in self.parsed_objs:
            name = self.parsed_objs[file].get(name)
            if name:return name[0]
        else:return None        
    def add_python_obj(self, name=None, obj=None, mode="w", runtime=False, file="main"):
        """
        file -> filename in the archive files added using add_file() method
        name -> the name which object should be saved
        obj -> object to be saved
        mode -> mode is an optional string, "w" means create/overwrite python object where "x" means create python object, does nothing if exists
        runtime -> flag to indicate whether to execute the code at runtime
        """
        if mode == "x" and name in self.python_objs.get(file, {}):
            return
        
        self.python_objs.setdefault(file, {})[name] = obj
        
        if not runtime:
            obj_tag = f"\n<[{name}]python.object[*]>"
            if obj_tag in self.hds_codes[file]:
                new_code = []
                on_eval = False
                for line in self.hds_codes[file].split("\n"):
                    if line.startswith("py_eval:"):
                        on_eval = True
                    elif not line.startswith(" "):
                        on_eval = False

                    if not on_eval and re.match(fr"\s*?{obj_tag}\s*?\w*?.*?\w*?.*\s*?", line):
                        new_code.append(f"{obj_tag}{name}.py.obj</[{name}]python.object[*]>")
                    else:
                        new_code.append(line)
                
                self.hds_codes[file] = "\n".join(new_code)
            else:
                self.hds_codes[file.split(".hds")[0]] += f"{obj_tag}{name}.py.obj</[{name}]python.object[*]>"
                        
    def get_python_obj(self,name,file="main"):
        if name in self.read_python_objs[file].keys():
            return self.read_python_objs[file][name]

    def delete_variables(self,file="main"):
        for k,v in self.iter_vars():
            self.delete_variable(k,file)
    
    """
        def compress_file(self,var_name,filename,mode="w"):
            ""
    name -> the name which object should be saves\n
    value -> object to be saves\n
    mode -> mode is a optional string, "w" means create/overwrite python object where "x" means create file, does nothing if exists
            ""   
            if mode=="x":    
                if name not in self.compressed_files.keys():
                    self.compressed_files[var_name] = filename
            else:
                self.compressed_files[var_name] = filename
    """
    def add_obj(self,obj:HDSObject,file="main"):
        self.objects[file].append(obj)
        self.hds_codes[file]+=obj._finalize()[0]
    def set_variable(self, var=None, value=None, mode="w", runtime=False, file="main"):
        # Determine the data type of the value
        data_type = type(value).__name__

        # If the value is a dictionary or a TraceDict, attach an on_change callback
        if isinstance(value, TraceDict):
            value.on_change = lambda ndict: self.set_variable(var, ndict, mode, runtime, file)

        # If the value is a list or a TraceList, attach a callback
        elif isinstance(value, TraceList):
            value.callback = lambda nlist: self.set_variable(var, nlist, mode, runtime, file)

        # If the value is None, set the data type to "NoneType"
        elif value is None:
            data_type = "NoneType"

        # If the data type is not recognized, raise an exception
        elif data_type not in ["str", "int", "float", "bool", "tuple", "list", "dict"]:
            invalidDataType(value)

        # Add the variable to the dictionary
        if mode == "x" and var in self.variables[file]:
            pass  # do nothing if the variable already exists
        else:
            self.variables[file][var] = [value, data_type]

        # If runtime is False, update the code in the file
        if not runtime:
            # Format the value for the code
            new_value = f'"{value}"' if data_type == "str" else str(value)

            # Check if the variable already exists in the code
            if var in self.var_idxs[file]:
                new_code = self.hds_codes[file].split("\n")
                new_code[self.var_idxs[file][var]] = f"{var} = {new_value}"
                self.hds_codes[file] = "\n".join(new_code)
            else:
                self.var_idxs[file][var] = len(self.hds_codes[file].split("\n"))
                
                self.hds_codes[file]+= f"\n{var} = {new_value}"
            
        return self.get_variable(file, var)

    def update_target_class(self,target_class):
        """
Overwrites the variables and python_objects in HyperDataStorage to the target_class
        """
        for file in self.files:
            if file[0].endswith(".hds"):            
                subcls = _File()
                for var,value in self.variables[file[0].split(".hds")[0]].items():
                    value, format = value
                    setattr(subcls,var,value)
                setattr(target_class,file[0].split(".hds")[0],subcls)
        for file in self.files:
            if file[0].endswith(".hds"):
                subcls = _File()
                for name,obj in self.read_python_objs[file[0].split(".hds")[0]].items():
                    setattr(subcls,name,obj)
                setattr(target_class,file[0].split(".hds")[0],subcls)
    def get_variable(self,var=None,check_temporary_vars=True,file="main"):
        if file in self.variables:
            var = self.variables[file].get(var)
            if var:return var[0]
            else:
                if check_temporary_vars:
                    return self.temp_vars[file].get(var)
        else:return None
   
    def set_pyeval(self,name,data="""print("HDS!")""",file="main"):
            self.open_file(f"{name}.py.eval","w").write(data)
            splitted = self.hds_codes[file].split("\n")
            code = "py.eval::"+name+".py.eval"
            if code not in splitted:
                self.hds_codes[file]+="\n"+code
    def add_import(self,import_filename="test",file="main"):
        self.imports["hdsimports"][file].append(import_filename+".hds")
        if "import "+import_filename+".hds" not in self.hds_codes[file].split("\n"):
            self.hds_codes[file]+=("\n"+"import "+import_filename+".hds")
    def py_eval_func_export(self,variable, value, type_="temp_variables",file="main",*args, **kwargs):
        
        if type_ == "variables":self.set_variable(variable,value,runtime=kwargs.pop("runtime") if "runtime" in kwargs else True,file=file,*args,**kwargs)
        elif type_ == "python_object":self.read_python_objs[file][variable] = value
        elif type_ == "temp_variables":self.temp_vars[file][variable] = value
    def init_file(self,file):
        if file.split(".hds")[0] not in self.variables:
            self.temp_vars[file.split(".hds")[0]] = {}
            self.variables[file.split(".hds")[0]] = {}
            self.read_python_objs[file.split(".hds")[0]] = {}
            self.python_objs[file.split(".hds")[0]] = {}         
            self.imports["pyimports"][file.split(".hds")[0]] = {}
            self.imports["hdsimports"][file.split(".hds")[0]] = {}
            self.pyevals[file.split(".hds")[0]] = []
            self.file_globals[file.split(".hds")[0]] = {}
            self.hds_codes[file.split(".hds")[0]] = ""
            self.hds_codes[file.split(".hds")[0]]+=DEFAULT_HDS_CODE_WITHOUT_DEVLOGS
            self.var_idxs[file.split(".hds")[0]] = {}
            self.objects[file.split(".hds")[0]] = []
            self.parsed_objs[file.split(".hds")[0]] = {}

    def custom_parse(self, add_python_objs_to_vars = True, target_class=None,path=None,zipf=None,allow_pyevals=True,eval_kwargs={}):

        for file in self.hdsobject.files():

            if file.endswith('.hds'):
                self.init_file(file)
                self.logger = Logger(False,file)
                self.custom_parse_one_file(file,self.hdsobject.read(file,"rb").decode("utf-8").split("\n"),add_python_objs_to_vars,path,target_class,self.hdsobject.archive,zipf,allow_pyevals,eval_kwargs)
            elif not file.endswith(".py.obj") and not file.endswith(".py.eval"):
                self.add_file(file)
    def custom_parse_one_file(self,file, data, add_python_objs_to_vars = True, path=None,target_class=None,archive=True,zipf=None,allow_pyevals=True,eval_kwargs={}):
        self.outputs = []  
        
        eval_command = False
        if target_class:
            subcls = _File()
            setattr(target_class,file.split(".hds")[0],subcls)
        parse_data = {"evaluation":False}
    
        for line_num,line in enumerate(data):

                    if not eval_command:
                        if line.strip() != "" and not line.startswith("#"):
                            
                            parse_data["evaluation"] = True if line.startswith(" ") else False
                            if line.strip().startswith("devlogs"):
                                if line.split("devlogs ")[1].strip().lower() == "true":self.logs = True
                                else:self.logs = False
                                self.logger.logs = self.logs
                            # OLD REGEX: [a-z]+\s*\=\s*[\{\[\(]?[a-z]*[0-9]*\s*
                            elif re.match(r"import\s*.*",line):
                                import_fn = line.split("import ")[1]
                                self.add_import(import_fn,file.split(".hds")[0])
                                if not parse_data["evaluation"]:self.hdsimport(file.split(".hds")[0],import_fn,zipf,archive)
                                self.logger.baselog("Importing "+import_fn)
                            elif line.startswith("py.eval::"):
                                filename = line.split("py.eval::")[1]
                                name = filename.split(".py.eval")[0]                                
                                if allow_pyevals:
                                    self.file_globals[file.split(".hds")[0]].update(self.temp_vars[file.split(".hds")[0]])
                                    self.file_globals[file.split(".hds")[0]].update(self.variables[file.split(".hds")[0]])
                                    self.file_globals[file.split(".hds")[0]].update(self.read_python_objs[file.split(".hds")[0]])
                                    self.file_globals[file.split(".hds")[0]].update(self.imports["hdsimports"][file.split(".hds")[0]])
                                    
                                    self.file_globals[file.split(".hds")[0]].update({
                                        "export":lambda    variable,value,type_ = "variables",*args,**kwargs: self.py_eval_func_export(variable,value,type_,file.split(".hds")[0],*args,**kwargs),
                                        "export_to":self.py_eval_func_export,
                                        "__file__":file,
                                    })                  
                                    self.file_globals[file.split(".hds")[0]].update(eval_kwargs)      
  
                                    data = self.open_file(filename,"r").read()       
                                    self.set_pyeval(name,data,file=file.split(".hds")[0])
                                    self.logger.baselog("Running pyeval: "+name)
                                    exec(data,self.file_globals[file.split(".hds")[0]])
                                else:
                                    self.logger.baselog("Skipping pyeval: "+name+" (allow_pyevals is False)")                        
                            elif re.match(r"([\w]*[\d]*)\s*:\s*",line):
                                name,obj = object_initializer(data,line,file,target_class,self)
                                
                                self.parsed_objs[file.split(".hds")[0]][name] = [obj,line_num]
                                if target_class:setattr(getattr(target_class,file.split(".hds")[0]),name,obj)
                            elif re.match(r".+\s*\=\s*[\{\[\(]*.*\s*",line):
                                variable,value,format_ = parse_variable(self,line,data,get_var_format(line),target_class,file,line_num)
                                self.logger.vlog(variable,format_,value,line_num+1,line)
                            elif re.match(r'\s*?\<\[\w*\]python.object\[\*\]\>\s*?\w*?.*?\w*?.*\s*?',line):
                                if not parse_data["evaluation"]:
                                    span = re.search(r'\<\[\w*\]',line).span()
                                    name = line[span[0]+2:span[1]-1]
                                    filename = line.split(f"<[{name}]python.object[*]>")[1].split(f"</[{name}]python.object[*]>")[0]
                                    try:obj = self.serializer_module.loads(self.hdsobject.read(filename,"rb"),*self.serializer_load_args,**self.serializer_load_kwargs)
                                    except Exception as e:
                                        
                                        raise Exception(str(e.with_traceback(None))+("\n\n\033[31mMost likely the object is defined after hds.read method\033[0m" if colorama else "\n\n31mMost likely the object is defined after hds.read method"))
                                    self.read_python_objs[file.split(".hds")[0]][name] = obj
                                    self.add_python_obj(name, obj,file=file.split(".hds")[0])
                                    if(add_python_objs_to_vars):self.temp_vars[file.split(".hds")[0]][name] = obj
                                    if target_class and file.endswith(".hds"):
                                        setattr(subcls,name,obj)
                                    self.logger.baselog("Loading python object: "+name)
                            """
                            elif re.match(r"\s*?\<\[\w*\]compressed.file\[\*\]\>\s*?\w*?.*?\w*?.*\s*",line):
                                span = re.search(r'\<\[\w*\]',line).span()
                                name = line[span[0]+2:span[1]-1]
                                filename = line.split(f"<[{name}]compressed.file[*]>")[1].split(f"</[{name}]compressed.file[*]>")[0]
                                if not archive:
                                    return open(filename,"r+")                           
                                else:
                                    zipf = zipfile.ZipFile(archive_path)
                                    data = zipf.read(filename)
                                    try:obj = io.StringIO(data)
                                    except:obj = io.BytesIO(data)
                                    obj.iowrite = obj.write
                                    obj.iowritelines = obj.writelines
                                    obj.ioread = obj.read
                                    obj.ioreadlines = obj.readlines
                                    obj.filename = filename
                                    obj.hds_var_archive_path = archive_path
                                    def update(obj):
                                        with zipfile.ZipFile(obj.hds_var_archive_path) as zipf:
                                            if obj.filename in zipf.filelist:
                                                zipf.setpassword
                                    def operate(obj,process="write",*args,**kwargs):
                                        try:return getattr(obj,process)(*args,**kwargs)
                                        except:return getattr(obj,process)
                                    obj.write = lambda *args,**kwargs:operate(obj,"write",*args,**kwargs)
                                    if(add_python_objs_to_vars):self.temp_vars[file][name] = obj
                                    if target_class:setattr(subcls,name,obj)
                            """                    
        if target_class and file.endswith(".hds"):setattr(target_class,file.split(".hds")[0],subcls)  
    
    def save(self,devlogs=False,destination=None,string_compression_func=lambda x,is_hds_code:x,close_temp_folder=False,pop_empty_lines=True):
        """

        """
        if destination:self.hdsobject = destination
        for file in self.files:
            data = file[1]
            file = file[0]
            if file.endswith(".hds"):
                
                        data = string_compression_func(self.hds_codes[file.split(".hds")[0]],True)

                        updated_hds_code = self.hds_codes[file.split(".hds")[0]].split("\n")
                        updated_hds_code.insert(0,"devlogs "+str(devlogs))
                        data = self.hds_codes[file.split(".hds")[0]] = "\n".join(updated_hds_code)

                        for name,obj in self.python_objs[file.split(".hds")[0]].items():
                            self.hdsobject.write(name+".py.obj",pickle.dumps(obj,*self.serializer_dump_args,**self.serializer_dump_kwargs),"wb")
                        if pop_empty_lines:data = "\n".join(filter(lambda x:True if x.strip()!="" else False,data.split("\n")))

            self.hdsobject.write(file,data)
        self.hdsobject.close(close_tempfolder=close_temp_folder)

def _new_target_class() -> object:
    class Data(TargetClass):
        def __init__(self):
            pass    
    return Data()

if __name__ == "__main__":
    # Creating HyperDS instance
    hds = HyperDataStorage("test.hds")
    # Trying to read archive 
    # ignores every errors while reading the file eg. file does not exists because of parameter file_read_errors: str = "ignore" while creating instance     
    hds.read_archive("test.hds")
    # creating a target class which could be used to read variables and python objects
    data = hds.new_target_class()
    # creating empty dict variable if variable "persons" does not exists  
    persons = hds.set_variable("persons",{},"x")
    # getting user input
    cmd = input(">> ")
    try:
        if cmd == "add":
            while True:
                name = input("Name: ")
                age = input("Age: ")
                # updating "persons" dict
                persons.update({name:age})
                # updating "persons" variable in target_class (variable data)
                hds.update_target_class(data)
        elif cmd == "get":
            # iterating through "persons" dict and printing their values
            for person,age in hds.get_variable("persons").items():
                print(person+" >> "+str(age))
    except KeyboardInterrupt:
        # Save all data as archive test.hds which may contain py.obj files if any python objects are added
        hds.save(devlogs=False)    