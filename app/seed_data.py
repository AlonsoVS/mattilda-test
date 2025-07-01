from datetime import date, datetime
from sqlmodel import Session, select
from app.database import engine
from app.models import School, Student, Invoice


def seed_data():
    """Seed the database with initial data"""
    with Session(engine) as session:
        # Check if data already exists
        existing_schools = session.exec(select(School)).first()
        if existing_schools:
            print("Database already seeded, skipping...")
            return

        # Create schools
        schools = [
            School(
                name="Lincoln Elementary School",
                address="123 Main Street",
                city="Springfield",
                state="Illinois",
                zip_code="62701",
                phone="(217) 555-0101",
                email="info@lincoln.edu",
                principal="Sarah Johnson",
                student_count=450,
                is_active=True
            ),
            School(
                name="Washington High School",
                address="456 Oak Avenue",
                city="Madison",
                state="Wisconsin",
                zip_code="53703",
                phone="(608) 555-0202",
                email="admin@washington.edu",
                principal="Michael Chen",
                student_count=1200,
                is_active=True
            ),
            School(
                name="Roosevelt Middle School",
                address="789 Elm Street",
                city="Portland",
                state="Oregon",
                zip_code="97201",
                phone="(503) 555-0303",
                email="contact@roosevelt.edu",
                principal="Jennifer Davis",
                student_count=680,
                is_active=True
            ),
            School(
                name="Jefferson Academy",
                address="321 Pine Road",
                city="Austin",
                state="Texas",
                zip_code="73301",
                phone="(512) 555-0404",
                email="office@jefferson.edu",
                principal="Robert Martinez",
                student_count=890,
                is_active=True
            ),
            School(
                name="Franklin Preparatory School",
                address="654 Cedar Lane",
                city="Denver",
                state="Colorado",
                zip_code="80202",
                phone="(303) 555-0505",
                email="hello@franklin.edu",
                principal="Lisa Thompson",
                student_count=320,
                is_active=True
            ),
            School(
                name="Adams Charter School",
                address="987 Birch Boulevard",
                city="Phoenix",
                state="Arizona",
                zip_code="85001",
                phone="(602) 555-0606",
                email="info@adams.edu",
                principal="David Wilson",
                student_count=540,
                is_active=True
            ),
            School(
                name="Hamilton Institute",
                address="147 Maple Drive",
                city="Seattle",
                state="Washington",
                zip_code="98101",
                phone="(206) 555-0707",
                email="admin@hamilton.edu",
                principal="Amanda Garcia",
                student_count=750,
                is_active=False
            ),
            School(
                name="Madison Community School",
                address="258 Walnut Street",
                city="Madison",
                state="Wisconsin",
                zip_code="53704",
                phone="(608) 555-0808",
                email="contact@madison.edu",
                principal="James Anderson",
                student_count=410,
                is_active=True
            )
        ]

        for school in schools:
            session.add(school)
        session.commit()

        # Create students
        students = [
            Student(
                first_name="Emma",
                last_name="Johnson",
                email="emma.johnson@email.com",
                phone="(217) 555-1001",
                date_of_birth=date(2010, 3, 15),
                grade_level=8,
                school_id=1,
                student_id_number="LIN001",
                enrollment_date=date(2023, 8, 15),
                guardian_name="Mary Johnson",
                guardian_phone="(217) 555-1000",
                guardian_email="mary.johnson@email.com",
                address="456 School Street",
                city="Springfield",
                state="Illinois",
                zip_code="62701",
                is_active=True
            ),
            Student(
                first_name="Liam",
                last_name="Chen",
                email="liam.chen@email.com",
                phone="(608) 555-2001",
                date_of_birth=date(2006, 7, 22),
                grade_level=12,
                school_id=2,
                student_id_number="WAS002",
                enrollment_date=date(2022, 8, 20),
                guardian_name="David Chen",
                guardian_phone="(608) 555-2000",
                guardian_email="david.chen@email.com",
                address="789 Student Avenue",
                city="Madison",
                state="Wisconsin",
                zip_code="53703",
                is_active=True
            ),
            Student(
                first_name="Sophia",
                last_name="Davis",
                email="sophia.davis@email.com",
                phone="(503) 555-3001",
                date_of_birth=date(2011, 11, 8),
                grade_level=7,
                school_id=3,
                student_id_number="ROO003",
                enrollment_date=date(2023, 9, 1),
                guardian_name="Jennifer Davis",
                guardian_phone="(503) 555-3000",
                guardian_email="jennifer.davis@email.com",
                address="321 Learning Lane",
                city="Portland",
                state="Oregon",
                zip_code="97201",
                is_active=True
            ),
            Student(
                first_name="Noah",
                last_name="Martinez",
                email="noah.martinez@email.com",
                phone="(512) 555-4001",
                date_of_birth=date(2008, 1, 30),
                grade_level=10,
                school_id=4,
                student_id_number="JEF004",
                enrollment_date=date(2023, 8, 25),
                guardian_name="Roberto Martinez",
                guardian_phone="(512) 555-4000",
                guardian_email="roberto.martinez@email.com",
                address="654 Education Drive",
                city="Austin",
                state="Texas",
                zip_code="73301",
                is_active=True
            ),
            Student(
                first_name="Olivia",
                last_name="Thompson",
                email="olivia.thompson@email.com",
                phone="(303) 555-5001",
                date_of_birth=date(2009, 9, 12),
                grade_level=9,
                school_id=5,
                student_id_number="FRA005",
                enrollment_date=date(2023, 8, 30),
                guardian_name="Lisa Thompson",
                guardian_phone="(303) 555-5000",
                guardian_email="lisa.thompson@email.com",
                address="987 Academy Road",
                city="Denver",
                state="Colorado",
                zip_code="80202",
                is_active=True
            ),
            Student(
                first_name="Ethan",
                last_name="Wilson",
                email="ethan.wilson@email.com",
                phone="(602) 555-6001",
                date_of_birth=date(2012, 5, 18),
                grade_level=6,
                school_id=6,
                student_id_number="ADA006",
                enrollment_date=date(2023, 8, 15),
                guardian_name="David Wilson",
                guardian_phone="(602) 555-6000",
                guardian_email="david.wilson@email.com",
                address="147 Charter Boulevard",
                city="Phoenix",
                state="Arizona",
                zip_code="85001",
                is_active=True
            ),
            Student(
                first_name="Ava",
                last_name="Garcia",
                email="ava.garcia@email.com",
                phone="(206) 555-7001",
                date_of_birth=date(2007, 12, 3),
                grade_level=11,
                school_id=7,
                student_id_number="HAM007",
                enrollment_date=date(2022, 9, 5),
                guardian_name="Amanda Garcia",
                guardian_phone="(206) 555-7000",
                guardian_email="amanda.garcia@email.com",
                address="258 Institute Street",
                city="Seattle",
                state="Washington",
                zip_code="98101",
                is_active=False
            ),
            Student(
                first_name="Mason",
                last_name="Anderson",
                email="mason.anderson@email.com",
                phone="(608) 555-8001",
                date_of_birth=date(2010, 4, 25),
                grade_level=8,
                school_id=8,
                student_id_number="MAD008",
                enrollment_date=date(2023, 8, 20),
                guardian_name="James Anderson",
                guardian_phone="(608) 555-8000",
                guardian_email="james.anderson@email.com",
                address="369 Community Circle",
                city="Madison",
                state="Wisconsin",
                zip_code="53704",
                is_active=True
            )
        ]

        for student in students:
            session.add(student)
        session.commit()

        # Create invoices
        invoices = [
            Invoice(
                invoice_number="INV-2024-001",
                student_id=1,
                school_id=1,
                amount=850.00,
                tax_amount=68.00,
                total_amount=918.00,
                description="Tuition fee for Spring semester 2024",
                invoice_date=date(2024, 1, 15),
                due_date=date(2024, 2, 15),
                payment_date=date(2024, 2, 10),
                status="paid",
                payment_method="bank_transfer",
                created_at=datetime(2024, 1, 15, 9, 0, 0),
                updated_at=datetime(2024, 2, 10, 14, 30, 0),
                notes="Payment received on time"
            ),
            Invoice(
                invoice_number="INV-2024-002",
                student_id=2,
                school_id=2,
                amount=1200.00,
                tax_amount=96.00,
                total_amount=1296.00,
                description="High school tuition and laboratory fees",
                invoice_date=date(2024, 1, 20),
                due_date=date(2024, 2, 20),
                payment_date=None,
                status="pending",
                payment_method=None,
                created_at=datetime(2024, 1, 20, 10, 0, 0),
                updated_at=datetime(2024, 1, 20, 10, 0, 0),
                notes="Reminder sent on 2024-02-15"
            ),
            Invoice(
                invoice_number="INV-2024-003",
                student_id=3,
                school_id=3,
                amount=750.00,
                tax_amount=60.00,
                total_amount=810.00,
                description="Middle school tuition and activity fees",
                invoice_date=date(2024, 1, 25),
                due_date=date(2024, 2, 25),
                payment_date=date(2024, 2, 22),
                status="paid",
                payment_method="credit_card",
                created_at=datetime(2024, 1, 25, 11, 0, 0),
                updated_at=datetime(2024, 2, 22, 16, 45, 0),
                notes="Paid via online portal"
            ),
            Invoice(
                invoice_number="INV-2024-004",
                student_id=4,
                school_id=4,
                amount=950.00,
                tax_amount=76.00,
                total_amount=1026.00,
                description="Academy tuition and technology fee",
                invoice_date=date(2024, 2, 1),
                due_date=date(2024, 3, 1),
                payment_date=None,
                status="overdue",
                payment_method=None,
                created_at=datetime(2024, 2, 1, 9, 30, 0),
                updated_at=datetime(2024, 3, 5, 8, 0, 0),
                notes="Second notice sent"
            ),
            Invoice(
                invoice_number="INV-2024-005",
                student_id=5,
                school_id=5,
                amount=1100.00,
                tax_amount=88.00,
                total_amount=1188.00,
                description="Preparatory school tuition",
                invoice_date=date(2024, 2, 5),
                due_date=date(2024, 3, 5),
                payment_date=date(2024, 3, 1),
                status="paid",
                payment_method="check",
                created_at=datetime(2024, 2, 5, 12, 0, 0),
                updated_at=datetime(2024, 3, 1, 10, 15, 0),
                notes="Check #1234 received"
            ),
            Invoice(
                invoice_number="INV-2024-006",
                student_id=6,
                school_id=6,
                amount=680.00,
                tax_amount=54.40,
                total_amount=734.40,
                description="Charter school tuition and supplies",
                invoice_date=date(2024, 2, 10),
                due_date=date(2024, 3, 10),
                payment_date=None,
                status="pending",
                payment_method=None,
                created_at=datetime(2024, 2, 10, 14, 0, 0),
                updated_at=datetime(2024, 2, 10, 14, 0, 0),
                notes="First notice"
            ),
            Invoice(
                invoice_number="INV-2024-007",
                student_id=7,
                school_id=7,
                amount=1050.00,
                tax_amount=84.00,
                total_amount=1134.00,
                description="Institute tuition and graduation fees",
                invoice_date=date(2024, 2, 15),
                due_date=date(2024, 3, 15),
                payment_date=None,
                status="cancelled",
                payment_method=None,
                created_at=datetime(2024, 2, 15, 15, 0, 0),
                updated_at=datetime(2024, 2, 20, 9, 0, 0),
                notes="Student transferred to another school"
            ),
            Invoice(
                invoice_number="INV-2024-008",
                student_id=8,
                school_id=8,
                amount=780.00,
                tax_amount=62.40,
                total_amount=842.40,
                description="Community school tuition",
                invoice_date=date(2024, 2, 20),
                due_date=date(2024, 3, 20),
                payment_date=date(2024, 3, 18),
                status="paid",
                payment_method="cash",
                created_at=datetime(2024, 2, 20, 16, 0, 0),
                updated_at=datetime(2024, 3, 18, 11, 30, 0),
                notes="Cash payment received at school office"
            )
        ]

        for invoice in invoices:
            session.add(invoice)
        session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    from app.database import create_db_and_tables
    create_db_and_tables()
    seed_data()
