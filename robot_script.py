import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select_set(True) # ...excepto el buscado

def seleccionarObjeto2(nombreObjeto1,nombreObjeto2): # Seleccionar 2 objetos por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto1].select_set(True) #seleccionamos los dos que queremos
    bpy.data.objects[nombreObjeto2].select_set(True)

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
        
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(radius = 0.25, depth = 0.5, location = (0, 0, 0))
        Activo.renombrar(objName)
        
    def crearCamara(objName):
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0, 0, 0))
        Activo.renombrar(objName)


def crearPie():
    Objeto.crearCubo("Pie1")
    Seleccionado.escalar((1,1,0.2))
    
    Objeto.crearCubo("Joint1")
    Seleccionado.mover((0,0,0.15))
    Seleccionado.escalar((0.5,0.2,0.4))
    
    seleccionarObjeto2("Pie1","Joint1")
    bpy.ops.object.join()
    Activo.renombrar("Pie1")
    
    Objeto.crearCilindro("Axis1")
    Seleccionado.escalar((0.1,0.1,0.7))
    Seleccionado.mover((0,0,0.2))
    Activo.rotar((0,3/2*3.14159,0))
    
    seleccionarObjeto2("Pie1","Axis1")
    bpy.ops.object.join()
    Activo.renombrar("Pie1")
    
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
 
    borrarObjetos()
    
    Objeto.crearCamara("miCamara")
    Seleccionado.mover((6,-4,4))
    Activo.rotar((1.3,0,1))
    bpy.context.object.data.lens = 32
    
    crearPie()