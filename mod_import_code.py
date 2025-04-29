import importlib.util
import sys

def execute_pyc(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module)


#execute_pyc('./mods/modname/b.pyc')


mods
|\-amod
| |-mod.json
| |-entrypoint.pyc
| |-othercode.pyc
| |\-otherstuff
| | |-import1.pyc
| | \-import2.pyc
|  \-textures
|   |-texture1.png
|   |-texture2.png



mod.json:
{
  'entrypoints':[
    'entrypoint.pyc'
  ],
  'name':"name goes here",
  'description':"description goes here"
  'require':[
    'requiredmod'
  ],
  'require_not':[
    'incompatiblemod'
  ],
  'suggest':[
    'suggestedmod'
  ],
  'mod_id':'amod'
}


require,require_not,suggest are all lists of mod ids
will cancel startup if not all mods listed in require are present
will cancel startup if any mods listed in require_not are present
will load after mods in require and suggest
if circular loading detected, will cancel startup
entrypoints is a list of paths to files relative to the mod.json that startup first





entrypoint.py:
  REQUIRES=['amod:othercode.pyc'] # a list of all files that it uses. 
  TEXTURELIST=['amod:textures/texture1.png']
  REQUIREDGROUPS=['all','object_group']# a list of all required object groups. If a group doesn't already exist, it is created.
  REQUIREDCLASSES={'baseSprite':'pg.sprite.Sprite'}#list of all classes to give the main function
  def main(amod_othercode,textureids:List[int],obj_groups:dict, classes:dict):
    #amod_othercode is the first module imported in the REQUIRES list. The module is passed on to this point in the code. Order of the
    #requires list is the order of the arguments.

    #textureids is a list containing the opengl texture ids of each texture in TEXTURELIST, with order retained. Suggestion: Only put a texture in 
    #TEXTURELIST if you are planning to use it in that section of the code.

    #obj_groups is a dictionary keyed with the name of each object group requested and the values being the requested groups.

    #this function MUST return a tuple as follows:
    (
      {
        'classid':class_variable#classid can be an already existing class (for modifications to classes from other things)
        #always include a line of this form for all created classes if you intend on referencing them ANYWHERE else
      },
      {
        'tickingfunction':('group_ticked',function_used_to_tick,groupids:List,tick_every:List[int]=1)
        #adds a new function to the update loop of the form
        #for i in groups[arg0]:
        #  arg1(i, *[groups[g] for g in arg2])
        #
        #that executes every tick_every frames. tick_every is optional and defaults to 1.
      },
      {
        'roomid':roomdata#roomdata is the data to pass when creating a room. If room roomid already exists, will attempt to overwrite. If the new
        #room is of a different size than the old one or doesn't have all of the connectors from the original, mod loading will fail.
        #if room roomid already exists, will leave old values unchanged if the new value is None
      },
      [
        ('roomid1','roomid2',id1:int,id2:int)#Attempts to link connector id1 of roomid1 to connector id2 of roomid2. If roomids are invalid or the
        # connectorids are invalid, modloading will fail.
      ],
      
    )
    

