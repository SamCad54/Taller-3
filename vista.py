from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QListWidget, QMessageBox

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 350, 250)
        self.setWindowTitle("Login")
        self.init_form()

    def init_form(self):
        self.is_logged = False
        
        user_label = QLabel(self)
        user_label.setText("Usuario: ")
        user_label.move(20, 50)

        self.user_input = QLineEdit(self)
        self.user_input.move(120, 50)
        
        password_label = QLabel(self)
        password_label.setText("Contraseña: ")
        password_label.move(20, 100)

        self.password_input = QLineEdit(self)
        self.password_input.move(120, 100)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.check_view_password = QCheckBox(self)
        self.check_view_password.setText("Ver contraseña")
        self.check_view_password.move(120, 140)
        
        login_button = QPushButton(self)
        login_button.setText("Login")
        login_button.move(20, 180)

        layout = QVBoxLayout(self)
        layout.addWidget(user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.check_view_password)
        layout.addWidget(login_button)

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Main View")

        self.patient_form = QWidget(self)

        layout = QVBoxLayout(self.patient_form)

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.age_input = QLineEdit()
        self.id_input = QLineEdit()

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Apellido:", self.surname_input)
        form_layout.addRow("Edad:", self.age_input)
        form_layout.addRow("Identificación:", self.id_input)

        layout.addLayout(form_layout)

        add_button = QPushButton("Agregar Paciente", self)
        layout.addWidget(add_button)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.patient_list = QListWidget()
        layout.addWidget(self.patient_list)

        delete_button = QPushButton("Eliminar Paciente", self)
        layout.addWidget(delete_button)

        logout_button = QPushButton("Logout", self)
        layout.addWidget(logout_button)

        self.setLayout(layout)