import sys
from PyQt5.QtWidgets import QApplication
from modelo import ModeloUsuarios
from vista import VistaLogin, VistaPrincipal
from controlador import Controlador

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    modelo = ModeloUsuarios()
    vista_login = VistaLogin()
    vista_principal = VistaPrincipal()
    controlador = Controlador(modelo, vista_login, vista_principal)
    
    vista_login.show()
    
    sys.exit(app.exec_())