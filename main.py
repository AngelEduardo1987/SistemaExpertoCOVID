# se importa la paqueteria que hace posible la conexion con el lenguaje prolog
from pyswip import Prolog
#se importa libreria de python para emitir fechas
from datetime import date

#se crea una instancia del metodo prolog
prolog= Prolog()

#impresion de mensaje de bienvenida y descripcion del sistema experto
print("\tSISTEMA DE LOCALIZACION DE PACIENTES DE COVID-19")
print("El sistema localiza a pacientes del COVID-19 entre los")
print("diferentes hospitales de los diferentes estados de la Republica")
print("para informar de su localizacion y estado de salud")

#se crea variable para controlar el bucle, en caso de que el usuario introduzca un campo vacio
paciente=""
inicio="Y"

while inicio=="Y":

    #inicio el ciclo solicitando campo "NOMBRE" y verificando que el campo
    while paciente=="":
        paciente =input("Inserte un nombre y apellido: ")
        print()
        print("\t*****************************************")

    # se eliminan espacios entre el nombre y apellidos
    query=paciente.replace(" ","")

    #se cargan los documentos prolog para las consultas
    prolog.consult("paciente.pl")
    #se realiza una consulta para verificar que el nombre introducido exista entre la lista de pacientes
    result = bool(list(prolog.query("paciente(" + query + ")")))
    # si existe se realizan las busquedas adicionales
    if result==True:
        #se emite un mensaje que el paciente esta registrado
        print("\tEl paciente "+ paciente+ " esta registrado")
        #se carga el archivo edades.pl para ser analizado
        prolog.consult("edades.pl")
        #se construye la consulta
        for valor in prolog.query("edad(" + query + ",Y)"):
            #se imprime la edad del paciente
            print("\tEdad: ",valor["Y"])
        #se carga el archivo status.pl para ser analizado y conocer el estado del paciente   
        prolog.consult("status.pl")
        # se crea y carga la consulta
        for valor in prolog.query("status(" + query + ",Y)"):
            # se emite el resultado y se almacena en la variable n
            print("\tStatus: ",valor["Y"])
            n = valor["Y"]
            #se carga el archivo hospital.pl para ser analizado
        prolog.consult("hospital.pl")
        #se crea la consulta para conocer en que hospital se encuentra el paciente
        for valor in prolog.query("hospital(" + query + ",Y)"):
            #se almacena el hospital para luego conocer el estado en el que se encuentra el hospital
            hospital = valor["Y"]
            #se imprime el nombre del hospital
            print("\tHospital: ",valor["Y"])
            #se genera el query para conocer la entidad federativa del hospital
        for valor in prolog.query("estado(" + hospital + ",Y)"):
            # se emite la entidad federativa
            print("\tEstado: ",valor["Y"])
            #se almacena la entidad
            estado = valor["Y"]
            # se crea la consulta para saber en que ciudad se encuentra el hospital
        for valor in prolog.query("ciudad(" + estado + ",Y)"):
            # se emite la ciudad en donde se encuentra el hospital
            print("\tCiudad: ",valor["Y"])
            # se analiza el estado del ṕaciente para estimar una fecha de alta
            if(n == 'recuperado'):
                alta= date.today()
                print("\tFecha de Alta: ", alta )
            else:
                #en caso de contrario se le notifica al usuario
                print("\tFecha de Alta: No establecida")
    # si no se encuentra el paciente se emite el mensaje
    else:
        print("El paciente "+ paciente+ " No ha sido registrado")
    print("\t****************************************")
    print()
    inicio= input("¿Desea continuar? y/n: ")
    if (inicio!="y"):
        inicio="N"
        print("Sistema Finalizado")
    else:
        inicio="Y"
        query=""
        paciente=""

