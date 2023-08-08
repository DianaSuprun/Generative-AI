from flask import Flask, jsonify, request, render_template
import pandas as pd
class TutorPreparation():


    def inputer_themes(self):
        themes = pd.read_csv('number_of_themes.csv').to_dict()
        return themes

    @staticmethod
    def number_of_questions():
        return int(input("Enter the number of questions: "))

    @staticmethod
    def level_of_questions():
        return int(input("Enter the level of questions: "))