import json
from datetime import datetime

class EstonianPeople:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        self.today = datetime.today()
        self.total_people = len(self.data)
        self.longest_name = ""
        self.longest_name_length = 0
        self.oldest_living_person = None
        self.oldest_living_age = 0
        self.oldest_living_birthdate = ""
        self.oldest_deceased_person = None
        self.oldest_deceased_age = 0
        self.oldest_deceased_birthdate = ""
        self.oldest_deceased_deathdate = ""
        self.actors_count = 0
        self.born_1997_count = 0
        self.unique_occupations = set()
        self.names_more_than_two_parts_count = 0
        self.same_birth_and_death_month_day_count = 0
        self.living_count = 0
        self.deceased_count = 0

        self.process_data()

    def process_data(self):
        for person in self.data:
            # Longest name
            if len(person['nimi']) > self.longest_name_length:
                self.longest_name = person['nimi']
                self.longest_name_length = len(person['nimi'])

            # Oldest living and deceased person
            birth_date = datetime.strptime(person['sundinud'], "%Y-%m-%d")
            if person['surnud'] == "0000-00-00":
                self.living_count += 1
                age = self.calculate_age(birth_date, self.today)
                if age > self.oldest_living_age:
                    self.oldest_living_age = age
                    self.oldest_living_person = person['nimi']
                    self.oldest_living_birthdate = person['sundinud']
            else:
                self.deceased_count += 1
                death_date = datetime.strptime(person['surnud'], "%Y-%m-%d")
                age = self.calculate_age(birth_date, death_date)
                if age > self.oldest_deceased_age:
                    self.oldest_deceased_age = age
                    self.oldest_deceased_person = person['nimi']
                    self.oldest_deceased_birthdate = person['sundinud']
                    self.oldest_deceased_deathdate = person['surnud']

            # Actors count
            if 'näitleja' in person['amet']:
                self.actors_count += 1

            # Born in 1997
            if birth_date.year == 1997:
                self.born_1997_count += 1

            # Unique occupations
            self.unique_occupations.add(person['amet'])

            # Names with more than two parts
            if len(person['nimi'].split(' ')) > 2:
                self.names_more_than_two_parts_count += 1

            # Same birth and death month and day
            if person['surnud'] != "0000-00-00":
                if birth_date.strftime('%m-%d') == death_date.strftime('%m-%d'):
                    self.same_birth_and_death_month_day_count += 1

    def get_total_people(self):
        return self.total_people

    def get_longest_name(self):
        return self.longest_name, self.longest_name_length

    def get_oldest_person(self, alive=True):
        if alive:
            return self.oldest_living_person, self.oldest_living_age, self.oldest_living_birthdate
        else:
            return self.oldest_deceased_person, self.oldest_deceased_age, self.oldest_deceased_birthdate, self.oldest_deceased_deathdate

    def get_actors_count(self):
        return self.actors_count

    def born_in_year(self, year):
        if year == 1997:
            return self.born_1997_count
        return 0

    def get_unique_occupations(self):
        return len(self.unique_occupations)

    def names_with_more_than_two_parts(self):
        return self.names_more_than_two_parts_count

    def same_birth_and_death_month_day(self):
        return self.same_birth_and_death_month_day_count

    def living_and_deceased_count(self):
        return self.living_count, self.deceased_count

    @staticmethod
    def calculate_age(birthdate, end_date):
        age = end_date.year - birthdate.year - ((end_date.month, end_date.day) < (birthdate.month, birthdate.day))
        return age
