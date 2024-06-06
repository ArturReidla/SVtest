import tkinter as tk
from tkinter import filedialog
from JSON_andmete_class import EstonianPeople
from datetime import datetime

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Eestlaste info")
        self.geometry("600x400")

        self.button = tk.Button(self, text="Ava fail", command=self.open_file)
        self.button.pack(pady=10)

        self.info_label = tk.Label(self, text="")
        self.info_label.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                people_data = EstonianPeople(file_path)
                info = self.get_info(people_data)
                self.show_info(info)
            except Exception as e:
                self.info_label.config(text=f"Viga andmete laadimisel: {e}")

    def get_info(self, people_data):
        total_people = people_data.get_total_people()
        longest_name, longest_name_length = people_data.get_longest_name()
        oldest_living_name, oldest_living_age, oldest_living_birthdate = people_data.get_oldest_person(alive=True)
        oldest_deceased_name, oldest_deceased_age, oldest_deceased_birthdate, oldest_deceased_deathdate = people_data.get_oldest_person(alive=False)
        actors_count = people_data.get_actors_count()
        born_1997 = people_data.born_in_year(1997)
        unique_occupations = people_data.get_unique_occupations()
        names_more_than_two_parts = people_data.names_with_more_than_two_parts()
        same_birth_death_month_day = people_data.same_birth_and_death_month_day()
        living_count, deceased_count = people_data.living_and_deceased_count()

        # Kasutame datetime teisendamiseks kuupäevad sobivasse vormingusse
        oldest_living_birthdate = datetime.strptime(oldest_living_birthdate, '%Y-%m-%d').strftime('%d.%m.%Y') if oldest_living_birthdate else ""
        oldest_deceased_birthdate = datetime.strptime(oldest_deceased_birthdate, '%Y-%m-%d').strftime('%d.%m.%Y') if oldest_deceased_birthdate else ""
        oldest_deceased_deathdate = datetime.strptime(oldest_deceased_deathdate, '%Y-%m-%d').strftime('%d.%m.%Y') if oldest_deceased_deathdate else ""

        return {
            "Isikute arv kokku": total_people,
            "Kõige pikem nimi ja tähemärkide arv": f"{longest_name} ({longest_name_length})",
            "Kõige vanem elav inimene": f"{oldest_living_name} ({oldest_living_age}) sündinud: {oldest_living_birthdate}",
            "Kõige vanem surnud inimene": f"{oldest_deceased_name} ({oldest_deceased_age}) sündinud: {oldest_deceased_birthdate}, surnud: {oldest_deceased_deathdate}",
            "Näitlejate koguarv": actors_count,
            "Sündinud 1997 aastal": born_1997,
            "Erinevaid elukutseid": unique_occupations,
            "Nimi sisaldab rohkem kui kaks nime": names_more_than_two_parts,
            "Sünniaeg ja surmaaeg on sama v.a. aasta": same_birth_death_month_day,
            "Elavaid isikuid": living_count,
            "Surnud isikuid": deceased_count
        }

    def show_info(self, info):
        formatted_info = "\n".join([f"{key}: {value}" for key, value in info.items()])
        self.info_label.config(text=formatted_info)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
