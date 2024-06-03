from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QCheckBox
import sys
from modelo import PatientModel
from vista import LoginView, MainView

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.view.check_view_password.clicked.connect(self.toggle_password_visibility)
        self.view.findChild(QPushButton, "Login").clicked.connect(self.login)
        self.view.show()

    def toggle_password_visibility(self):
        if self.view.check_view_password.isChecked():
            self.view.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.view.password_input.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.view.user_input.text()
        password = self.view.password_input.text()

        if username == "admin123" and password == "contrasena123":
            self.view.is_logged = True
            self.view.close()
            self.main_controller = MainController()
        else:
            self.view.show_error("Usuario o contraseña incorrectos")

class MainController:
    def __init__(self):
        self.model = PatientModel()
        self.view = MainView()
        self.view.findChild(QPushButton, "Agregar Paciente").clicked.connect(self.add_patient)
        self.view.findChild(QPushButton, "Eliminar Paciente").clicked.connect(self.remove_patient)
        self.view.search_input.textChanged.connect(self.search_patients)
        self.view.findChild(QPushButton, "Logout").clicked.connect(self.logout)
        self.update_patient_list()
        self.view.show()

    def add_patient(self):
        name = self.view.name_input.text()
        surname = self.view.surname_input.text()
        age = self.view.age_input.text()
        patient_id = self.view.id_input.text()

        if not name or not surname or not age or not patient_id:
            self.view.show_error("Todos los campos son obligatorios")
            return

        if any(patient['id'] == patient_id for patient in self.model.patients):
            self.view.show_error("La identificación ya existe")
            return

        self.model.add_patient({'name': name, 'surname': surname, 'age': age, 'id': patient_id})
        self.view.show_error("Paciente agregado exitosamente")
        self.view.name_input.clear()
        self.view.surname_input.clear()
        self.view.age_input.clear()
        self.view.id_input.clear()
        self.update_patient_list()

    def remove_patient(self):
        selected_item = self.view.patient_list.currentItem()
        if selected_item:
            patient_name = selected_item.text().split(' ')[0]
            patient_id = next(p['id'] for p in self.model.patients if p['name'] == patient_name)
            self.model.remove_patient(patient_id)
            self.update_patient_list()
            self.view.show_error("Paciente eliminado exitosamente")

    def search_patients(self):
        query = self.view.search_input.text().lower()
        self.view.patient_list.clear()
        for patient in self.model.patients:
            if query in patient['name'].lower() or query in patient['surname'].lower():
                self.view.patient_list.addItem(f"{patient['name']} {patient['surname']}")

    def update_patient_list(self):
        self.view.patient_list.clear()
        for patient in self.model.patients:
            self.view.patient_list.addItem(f"{patient['name']} {patient['surname']}")

    def logout(self):
        self.view.close()
        self.login_controller = LoginController()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_controller = LoginController()
    sys.exit(app.exec_())