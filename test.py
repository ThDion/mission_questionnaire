import unittest
from unittest.mock import patch
import questionnaire
import os
import questionnaire_import 
import json
def additionner(a, b):
    return a + b

def conversion_nombre():
    num_str = input("Entrez un nombre : ")
    return int(num_str)

class TestUnitaireDemo(unittest.TestCase):
    def setUp(self):
        print("setup")

    def tearDown(self):
        print("teardown")

    def test_additionner_nombres_positifs(self):
        print("test_additionner1")
        self.assertEqual(additionner(5,10), 15)
        self.assertEqual(additionner(6,10), 16)
        self.assertEqual(additionner(6000,10), 6010)
    def test_additionner_nombres_negatifs(self):
        print("test_additionner2")
        self.assertEqual(additionner(-6,-10), -16)

    def test_conversion_nombre_valide(self):
       with patch("builtins.input", return_value="10"):
        self.assertEqual (conversion_nombre(),10)
       with patch("builtins.input", return_value="100"):
        self.assertEqual (conversion_nombre(),100)
    def test_conversion_entree_valide(self):
       with patch("builtins.input", return_value="abc"):
        self.assertRaises(ValueError, conversion_nombre)


class TestsQuestion(unittest.TestCase):
    def test_question_bonne_mauvaise_reponse(self):
       choix = ("choix1", "choix2", "choix3")
       q = questionnaire.Question("titre_question", choix, "choix2" )
       with patch("builtins.input", return_value="1"):
        self.assertFalse(q.poser(1, 1))
       with patch("builtins.input", return_value="2"):
        self.assertTrue(q.poser(1, 1))
       with patch("builtins.input", return_value="3"):
        self.assertFalse(q.poser(1, 1))

class TestsQuestionnaire(unittest.TestCase):
   def test_questionnaire_lancer_alien_debutant(self):
      filename = os.path.join("test_data","cinema_alien_debutant.json")
      q = questionnaire.Questionnaire.from_json_file(filename)
      self.assertIsNotNone(q)
      self.assertEqual(len(q.questions), 10)
      self.assertEqual(q.titre, "Alien")
      self.assertEqual(q.categorie, "Cinéma")
      self.assertEqual(q.difficulte, "débutant")
      with patch("builtins.input", return_value="1"):
        self.assertEqual(q.lancer(),1)

      #nb questions
      #titre, categorie, difficulte
      #patcher le input -> forcer de répondre à 1 -> score = 4
      #lancer

def test_questionnaire_format_invalide(self):
   filename = os.path.join("test_data","format_invalide1.json")
   q = questionnaire.Questionnaire.from_json_file(filename)
   self.assertIsNotNone(q)
   self.assertEqual(q.categorie, 'Inconnu')
   self.assertEqual(q.difficulte, 'Inconnu')
   self.assertIsNotNone(q.questions)
   
   filename = os.path.join("test_data","format_invalide2.json")
   q = questionnaire.Questionnaire.from_json_file(filename)
   self.assertIsNone(q)
   self.assertIsNotNone(q.questions)

   filename = os.path.join("test_data","format_invalide3.json")
   q = questionnaire.Questionnaire.from_json_file(filename)
   self.assertIsNone(q)


class TestImportQuestionnaire(unittest.TestCase):
   def test_import_format_json(self):
      questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json")

      filenames = ("animaux_leschats_confirme.json","animaux_leschats_debutant.json", "animaux_leschats_expert.json" )
      for filename in filenames:
        self.assertTrue (os.path.isfile(filename))
        file = open(filename, "r")
        json_data = file.read()
        file.close()
        try:
            data = json.loads(json_data)
        except:
            self.fail("Problème de désérialisation pour le fichier " + filename)    
        
        self.assertIsNotNone(data.get("titre"))
        self.assertIsNotNone(data.get("questions"))
        self.assertIsNotNone(data.get("difficulte"))
        self.assertIsNotNone(data.get("categorie"))

        for question in data.get("questions"):
           self.assertIsNotNone(question.get("titre"))
           self.assertIsNotNone(question.get("choix"))
           for choix in question.get("choix"):
              self.assertGreater(len(choix[0]), 0)
              self.assertTrue(isinstance(choix[1], bool))
              bonne_reponse = [i[0] for i in question.get("choix") if i[1]]
              self.assertEqual(len(bonne_reponse), 1)

              
        # titre, questions, difficulté, categorie
        # question - > titre, choix
            #choix - > longueur du titre > 0
            #      - >2ème champ est bien un bool isinstance(..., bool)
            #      - > il y a bien un seule bonne réponse
unittest.main()