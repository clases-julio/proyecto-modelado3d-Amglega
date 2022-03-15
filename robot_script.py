import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select_set(True) # ...excepto el buscado


def seleccionarObjetos(Objetos):
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    for object in Objetos: #for para seleccionar todo los que queremos
        bpy.data.objects[object].select_set(True)

def juntarObjetos(nombreObjeto1,nombreObjeto2): # Seleccionar 2 objetos por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto1].select_set(True) #seleccionamos los dos que queremos
    bpy.data.objects[nombreObjeto2].select_set(True)
    bpy.ops.object.join()
    Activo.renombrar(nombreObjeto1)

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.view_layer.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
def cortarObjeto(objetoPrincipal,objetoMascara):
    activarObjeto(objetoPrincipal)
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[objetoMascara]
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
def pintarObjeto(nombreObjeto,color):
        activarObjeto(nombreObjeto)
        material = bpy.data.materials.new("Mat")
        bpy.context.active_object.data.materials.append(material)
        bpy.context.object.active_material.diffuse_color = color

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


def crearEje(objName):
    Objeto.crearCilindro(objName)
    Seleccionado.escalar((0.1,0.1,0.7))
    Seleccionado.mover((0,0,0.2))
    Seleccionado.rotarY(3/2*3.14159)

def crearPie(objName):
    
    Objeto.crearCubo(objName)
    Seleccionado.escalar((1,1,0.2))
    crearEje("Axis1")
    
    Objeto.crearCubo("Joint1")
    Seleccionado.mover((0,0,0.15))
    Seleccionado.escalar((0.5,0.2,0.4))

    juntarObjetos(objName, "Joint1")
    
    Objeto.crearCubo("corte")
    Seleccionado.escalar((1,1,1))
    
    Objeto.crearCilindro("Top")
    Seleccionado.escalar((0.3,0.27,0.5))
    Seleccionado.mover((0,0,0.2))
    Activo.rotar((0,3/2*3.14159,0))
    
    cortarObjeto("Top","corte")
    borrarObjeto("corte")
    juntarObjetos(objName, "Top")
    
    cortarObjeto(objName,"Axis1")
    borrarObjeto("Axis1")

def crearPierna(objName):
    
    crearEje("Axis1")
    crearEje("Axis2")
    Seleccionado.mover((0,0,0.4))
    Objeto.crearCubo(objName)
    Seleccionado.escalar((0.6,0.5,1))
    Seleccionado.mover((0,0,0.4))
    
    cortarObjeto(objName,"Axis1")
    borrarObjeto("Axis1")
    
    cortarObjeto(objName,"Axis2") 
    borrarObjeto("Axis2")
    
def crearMuslo(objName):
    
    crearEje("Axis2")
    Seleccionado.mover((0,0,0.4))
    
    Objeto.crearCubo("Hole1")
    Seleccionado.escalar((0.6,0.6,1.2))
    Seleccionado.mover((0,0,0.4))
    Objeto.crearCubo("Joint2")
    Seleccionado.escalar((0.1,0.1,1))
    Seleccionado.mover((0,0,1))
    Objeto.crearEsfera("Ball1")
    Seleccionado.escalar((0.1,0.1,0.1))
    Seleccionado.mover((0,0,1.25))
    
    Objeto.crearCubo(objName)
    Seleccionado.escalar((0.65,0.7,1))
    Seleccionado.mover((0,0,0.8))
    
    cortarObjeto(objName,"Axis2") 
    borrarObjeto("Axis2")
    cortarObjeto(objName,"Hole1") 
    borrarObjeto("Hole1")
    
    juntarObjetos(objName, "Joint2")
    juntarObjetos(objName, "Ball1")
    
def crearCuerpo(objName):
    
    Objeto.crearCubo(objName)
    Seleccionado.escalar((2,0.7,2))
    Seleccionado.mover((0,0,1.7))
    
    Objeto.crearCubo("Hole1")
    Seleccionado.escalar((0.3,0.2,0.4))
    Seleccionado.mover((-0.35,0,1.25))
    
    Objeto.crearCubo("Hole2")
    Seleccionado.escalar((0.3,0.2,0.4))
    Seleccionado.mover((0.35,0,1.25))
    
    crearEje("Axis1")
    Seleccionado.escalar((1.5,1.5,1.5))
    Seleccionado.mover((0.5,0,1.7))
    
    crearEje("Axis2")
    Seleccionado.escalar((1.5,1.5,1.5))
    Seleccionado.mover((-0.5,0,1.7))
    
    cortarObjeto(objName,"Hole1") 
    borrarObjeto("Hole1")
    cortarObjeto(objName,"Hole2") 
    borrarObjeto("Hole2")
    cortarObjeto(objName,"Axis1") 
    borrarObjeto("Axis1")
    cortarObjeto(objName,"Axis2") 
    borrarObjeto("Axis2")
    
    seleccionarObjeto(objName)
    Seleccionado.mover((0,0,-0.05))


def crearBrazo(objName):
    
    Objeto.crearCilindro(objName)
    Seleccionado.escalar((0.7,0.7,0.3))
    Seleccionado.mover((0.58,0,1.85))
    Activo.rotar((0,3/2*3.14159,0))
       
    Objeto.crearCilindro("Codo1")
    Seleccionado.escalar((0.5,0.5,0.2))
    Seleccionado.mover((0.58,0,1.3))
    Activo.rotar((0,3/2*3.14159,0))

    crearEje("Axis1")
    Seleccionado.mover((0.5,0,1.1))
    
    cortarObjeto("Codo1","Axis1") 
    borrarObjeto("Axis1")
    
    Objeto.crearCubo("Hombro1")
    Seleccionado.escalar((0.2,0.4,0.7))
    Seleccionado.mover((0.58,0,1.55))
    
    juntarObjetos(objName, "Hombro1")
    juntarObjetos(objName, "Codo1")
    
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
 
    borrarObjetos()
    
    Objeto.crearCamara("miCamara")
    Seleccionado.mover((6,-4,4))
    Activo.rotar((1.3,0,1))
    bpy.context.object.data.lens = 32
    
    bpy.ops.object.light_add(type='SUN', radius=1, location=(1, -1, 2))
    bpy.context.object.data.energy = 70

    '''Pierna1'''
    crearPie("Foot1")

    crearPierna("Leg1")
    cortarObjeto("Leg1","Foot1")
    crearMuslo("Thigh1")
    crearEje("Axis1")
    crearEje("Axis2")
    Seleccionado.mover((0,0,0.4))
    
    seleccionarObjetos(("Foot1","Leg1","Thigh1","Axis1","Axis2"))
    Seleccionado.mover((0.35,0,0))
    
    pintarObjeto("Foot1",(0,0,1,1))
    pintarObjeto("Leg1",(0,1,1,1))
    pintarObjeto("Thigh1",(0,0,1,1))
    pintarObjeto("Axis1",(0,0,0,1))
    pintarObjeto("Axis2",(0,0,0,1))
    
    '''Pierna2'''
    
    crearPie("Foot2")
    crearPierna("Leg2")
    cortarObjeto("Leg2","Foot2")
    crearMuslo("Thigh2")
    crearEje("Axis3")
    crearEje("Axis4")
    Seleccionado.mover((0,0,0.4))
    
    seleccionarObjetos(("Foot2","Leg2","Thigh2","Axis3","Axis4"))
    Seleccionado.mover((-0.35,0,0))
    
    pintarObjeto("Foot2",(0,0,1,1))
    pintarObjeto("Leg2",(0,1,1,1))
    pintarObjeto("Thigh2",(0,0,1,1))
    pintarObjeto("Axis3",(0,0,0,1))
    pintarObjeto("Axis4",(0,0,0,1))
    
    
    '''Cuerpo'''
    
    crearCuerpo("Cuerpo1")
    
    crearEje("Axis5")
    Seleccionado.escalar((1,1.5,1.5))
    Seleccionado.mover((0.5,0,1.65))
    
    crearEje("Axis6")
    seleccionarObjeto("Axis6")
    Seleccionado.escalar((1,1.5,1.5))
    Seleccionado.mover((-0.5,0,1.65))
    
    pintarObjeto("Cuerpo1",(0,1,1,1))
    pintarObjeto("Axis5",(0,0,0,1))
    pintarObjeto("Axis6",(0,0,0,1))
    
    
    '''Brazo1'''
    
    crearBrazo("Brazo1")
    cortarObjeto("Brazo1","Axis5")
    pintarObjeto("Brazo1",(0,0,1,1))
    
    
    '''Brazo2'''
    
    crearBrazo("Brazo2")
    Seleccionado.mover((-1.16,0,0))
    cortarObjeto("Brazo2","Axis6")
    pintarObjeto("Brazo2",(0,0,1,1))
    
    