from os import path
from csv import DictReader
from io import StringIO

from django.contrib.auth.models import User
from django.test import TestCase

from paf.models import TypeCandidature, TypePlan, Dispositif
from paf.admin import TypeCandidatureResource, TypePlanResource, DispositifResource

from paf.models import Modalite, PublicCible, Theme, Module
from paf.admin import ModaliteResource, PublicCibleResource, ThemeResource, ModuleResource

class AdminImportTests(TestCase):

    def setUp(self):
        # Créer un administrateur
        user = User.objects.create_user(
            'admin',
            'admin@example.com',
            'password'
        )

        user.is_staff = True
        user.is_superuser = True
        user.save()

        # Se connecte en tant qu'admin
        self.client.login(username='admin', password='password')

    def test_import_typecandidature_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/type_de_candidature.csv',
        )

        url = '/admin/paf/typecandidature/import/'

        dataset = TypeCandidatureResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)

    def test_import_typeplan_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/type_de_plan.csv',
        )

        url = '/admin/paf/typeplan/import/'

        dataset = TypePlanResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)

    def test_import_dispositif_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/dispositifs.csv',
        )

        url = '/admin/paf/dispositif/import/'

        dataset = DispositifResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)

    def test_import_modalite_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/modalites.csv',
        )

        url = '/admin/paf/modalite/import/'

        dataset = ModaliteResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)


    def test_import_publiccible_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/public_cible.csv',
        )

        url = '/admin/paf/publiccible/import/'

        dataset = PublicCibleResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)

    def test_import_theme_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/themes.csv',
        )

        url = '/admin/paf/theme/import/'

        dataset = ThemeResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)

    def test_import_module_with_correct_csv(self):
        """
        Quand le fichier csv importé est correctement formaté, on doit retrouver
        des enregistrements cohérents en base de données.
        """

        import_format = '0' # csv

        filename = path.join(
            path.dirname(__file__),
            'data/valid/modules.csv',
        )

        url = '/admin/paf/module/import/'

        dataset = ModuleResource().export()
        export = StringIO(dataset.csv)

        with open(filename, 'r') as csv_file:

            data = {
                'input_format': import_format,
                'import_file': csv_file,
            }

            response = self.client.post(url, data)

            # La page existe bien
            self.assertEqual(response.status_code, 200)

            csv_reader = DictReader(csv_file)
            db_reader = DictReader(export)

            # Compare les enregistrements
            for csv_row, db_row in zip(csv_reader, db_reader): 
                self.assertEqual(csv_row, db_row)
