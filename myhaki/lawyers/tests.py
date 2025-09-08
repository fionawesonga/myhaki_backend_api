
# Create your tests here.
from django.test import TestCase
from django.core.exceptions import ValidationError
from lawyers.models import Lawyer, CPDPoint

class LawyerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="lawyer@example.com",
            role="lawyer",
            first_name="Lawyer",
            last_name="Test"
        )
        self.lawyer = Lawyer.objects.create(
            user_id=self.user,
            practice_number="LSK/2025/014967",
            specialization=["criminal"],
            longitude=36.8219,
            latitude=-1.2921,
            verified=True
        )

    def test_lawyer_creation(self):
        self.assertEqual(self.lawyer.user_id.email, "lawyer@example.com")
        self.assertEqual(self.lawyer.practice_number, "LSK/2025/014967")
        self.assertTrue(self.lawyer.verified)

    def test_invalid_user_role(self):
        invalid_user = User.objects.create(
            email="applicant@example.com",
            role="applicant",
            first_name="Applicant",
            last_name="Test"
        )
        with self.assertRaises(ValidationError):
            lawyer = Lawyer(user_id=invalid_user, practice_number="LSK/2025/014968", longitude=36.8219, latitude=-1.2921)
            lawyer.full_clean()

class CPDPointModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="lawyer@example.com", role="lawyer", first_name="Lawyer", last_name="Test")
        self.lawyer = Lawyer.objects.create(user_id=self.user, practice_number="LSK/2025/014967", longitude=36.8219, latitude=-1.2921)
        self.detainee_user = User.objects.create(email="detainee@example.com", role="detainee", first_name="Detainee", last_name="Test")
        self.detainee = Detainee.objects.create(user_id=self.detainee_user, id_number="12345678", gender="male")
        self.case = Case.objects.create(
            detainee_id=self.detainee,
            case_description="Test case",
            predicted_urgency_level="high",
            latitude=-1.2921,
            longitude=36.8219,
            stage="in_progress",
            status="pending"
        )
        self.cpd_point = CPDPoint.objects.create(
            lawyer_id=self.lawyer,
            case_id=self.case,
            description="Completed case #123",
            points_earned=1.0
        )

    def test_cpd_point_creation(self):
        self.assertEqual(self.cpd_point.lawyer_id.practice_number, "LSK/2025/014967")
        self.assertEqual(self.cpd_point.points_earned, 1.0)
