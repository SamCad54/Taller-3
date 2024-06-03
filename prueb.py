import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QLineEdit, QTextEdit, QWidget, QLabel, QCheckBox, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QListWidget
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QFont
from PyQt5.QtCore import Qt, QRegExp

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUi()

    def inicializarUi(self):
        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle("Login")
        self.generar_formulario()
        self.show()

    def generar_formulario(self):
        self.is_logged = False
        
        user_label = QLabel(self)
        user_label.setText("Usuario: ")
        user_label.setFont(QFont("Arial", 10))
        user_label.move(20, 50)

        self.user_input = QLineEdit(self)
        self.user_input.resize(250, 24)
        self.user_input.move(120, 50)
        
        password_label = QLabel(self)
        password_label.setText("Contraseña: ")
        password_label.setFont(QFont("Arial", 10))
        password_label.move(20, 100)

        self.password_input = QLineEdit(self)
        self.password_input.resize(250, 24)
        self.password_input.move(120, 100)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.check_view_password = QCheckBox(self)
        self.check_view_password.setText("Ver contraseña")
        self.check_view_password.move(120, 140)
        self.check_view_password.clicked.connect(self.mostrarContrasena)
        
        login_button = QPushButton(self)
        login_button.setText("Login")
        login_button.resize(320, 34)
        login_button.move(20, 180)
        login_button.clicked.connect(self.iniciar_mainview)

    def mostrarContrasena(self, clicked):
        if clicked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def iniciar_mainview(self):
        username = self.user_input.text()
        password = self.password_input.text()

        if username == "admin123" and password == "contrasena123":
            self.is_logged = True
            self.close()
            self.main_view = MainView()
            self.main_view.show()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.patients = []
        self.inicializarUi()
        self.cargar_pacientes()

    def inicializarUi(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Main View")

        self.patient_form = QWidget(self)
        self.setCentralWidget(self.patient_form)

        layout = QVBoxLayout(self.patient_form)

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.age_input = QLineEdit()
        self.age_input.setValidator(QIntValidator(0, 99))
        self.id_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Apellido:", self.surname_input)
        form_layout.addRow("Edad:", self.age_input)
        form_layout.addRow("Identificación:", self.id_input)

        layout.addLayout(form_layout)

        add_button = QPushButton("Agregar Paciente", self)
        add_button.clicked.connect(self.agregar_paciente)
        layout.addWidget(add_button)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre")
        self.search_input.textChanged.connect(self.buscar_pacientes)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.patient_list = QListWidget()
        layout.addWidget(self.patient_list)

        delete_button = QPushButton("Eliminar Paciente", self)
        delete_button.clicked.connect(self.eliminar_paciente)
        layout.addWidget(delete_button)

        logout_button = QPushButton("Logout", self)
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

    def agregar_paciente(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        age = self.age_input.text()
        patient_id = self.id_input.text()

        if not name or not surname or not age or not patient_id:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if any(patient['id'] == patient_id for patient in self.patients):
            QMessageBox.warning(self, "Error", "La identificación ya existe")
            return

        self.patients.append({'name': name, 'surname': surname, 'age': age, 'id': patient_id})
        self.guardar_paciente_en_archivo({'name': name, 'surname': surname, 'age': age, 'id': patient_id})
        QMessageBox.information(self, "Éxito", "Paciente agregado exitosamente")
        self.limpiar_formulario()
        self.actualizar_lista_pacientes()

    def limpiar_formulario(self):
        self.name_input.clear()
        self.surname_input.clear()
        self.age_input.clear()
        self.id_input.clear()

    def guardar_paciente_en_archivo(self, paciente):
        with open('pacientes.txt', 'a') as file:
            file.write(f"{paciente['name']},{paciente['surname']},{paciente['age']},{paciente['id']}\n")

    def cargar_pacientes(self):
        try:
            with open('pacientes.txt', 'r') as file:
                for line in file:
                    name, surname, age, patient_id = line.strip().split(',')
                    self.patients.append({'name': name, 'surname': surname, 'age': age, 'id': patient_id})
        except FileNotFoundError:
            pass

    def actualizar_lista_pacientes(self):
        self.patient_list.clear()
        for patient in self.patients:
            self.patient_list.addItem(f"{patient['name']} {patient['surname']}")

    def buscar_pacientes(self):
        query = self.search_input.text().lower()
        self.patient_list.clear()
        for patient in self.patients:
            if query in patient['name'].lower() or query in patient['surname'].lower():
                self.patient_list.addItem(f"{patient['name']} {patient['surname']}")

    def eliminar_paciente(self):
        selected_item = self.patient_list.currentItem()
        if selected_item:
            index = self.patient_list.row(selected_item)
            del self.patients[index]
            self.actualizar_lista_pacientes()
            QMessageBox.information(self, "Éxito", "Paciente eliminado exitosamente")
            self.guardar_pacientes_a_archivo()

    def guardar_pacientes_a_archivo(self):
        with open('pacientes.txt', 'w') as file:
            for patient in self.patients:
                file.write(f"{patient['name']},{patient['surname']},{patient['age']},{patient['id']}\n")

    def logout(self):
        self.close()
        self.login_view = Login()
        self.login_view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec_())