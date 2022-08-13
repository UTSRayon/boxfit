class Usuario():
    """nombre=str
    apellido=str
    direccion=str
    telefono=str
    correo=str
    inscripcion=float
    actividad=str
    precio=float
    horario=str
    fecha_inicio=str"""

    def asignarDatos(self, nombre, apellido, direccion, telefono, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo



    def __init__(self):
        print("")

    """def __init__(self,nombre,apellido,direccion,telefono,correo):
        self.nombre=nombre
        self.apellido=apellido
        self.direccion=direccion
        self.telefono=telefono
        self.correo=correo"""

        #inscripcion,actividad,precio,horario,fecha_inicio):
    def asingarTodo(self,codigo,nombre,apellido,direccion,telefono,correo,inscripcion,actividad,precio,horario,fecha_inicio):
        self.codigo=codigo
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.inscripcion = inscripcion
        self.actividad = actividad
        self.precio = precio
        self.horario = horario
        self.fecha_inicio = fecha_inicio




