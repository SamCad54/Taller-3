class PatientModel:
    def __init__(self):
        self.patients = []
        self.load_patients_from_file()

    def add_patient(self, patient):
        self.patients.append(patient)
        self.save_patient_to_file(patient)

    def remove_patient(self, patient_id):
        self.patients = [p for p in self.patients if p['id'] != patient_id]
        self.save_all_patients_to_file()

    def load_patients_from_file(self):
        try:
            with open('pacientes.txt', 'r') as file:
                for line in file:
                    name, surname, age, patient_id = line.strip().split(',')
                    self.patients.append({'name': name, 'surname': surname, 'age': age, 'id': patient_id})
        except FileNotFoundError:
            pass

    def save_patient_to_file(self, patient):
        with open('pacientes.txt', 'a') as file:
            file.write(f"{patient['name']},{patient['surname']},{patient['age']},{patient['id']}\n")

    def save_all_patients_to_file(self):
        with open('pacientes.txt', 'w') as file:
            for patient in self.patients:
                file.write(f"{patient['name']},{patient['surname']},{patient['age']},{patient['id']}\n")