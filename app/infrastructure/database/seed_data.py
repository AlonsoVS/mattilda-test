from datetime import date, datetime
from sqlmodel import Session, select
from app.infrastructure.database.connection import engine
from app.domain.entities.school import School
from app.domain.entities.student import Student
from app.domain.entities.invoice import Invoice


def seed_data():
    """Seed the database with initial data"""
    with Session(engine) as session:
        # Check if data already exists
        existing_schools = session.exec(select(School)).first()
        if existing_schools:
            print("Database already seeded, skipping...")
            return

        # Create schools
        schools_data = [
            {
                "name": "Lincoln Elementary School",
                "address": "123 Main Street",
                "city": "Springfield",
                "state": "Illinois",
                "zip_code": "62701",
                "phone": "(217) 555-0101",
                "email": "info@lincoln.edu",
                "principal": "Sarah Johnson",
                "student_count": 450,
                "is_active": True
            },
            {
                "name": "Washington High School",
                "address": "456 Oak Avenue",
                "city": "Madison",
                "state": "Wisconsin",
                "zip_code": "53703",
                "phone": "(608) 555-0202",
                "email": "admin@washington.edu",
                "principal": "Michael Chen",
                "student_count": 1200,
                "is_active": True
            },
            {
                "name": "Roosevelt Middle School",
                "address": "789 Elm Street",
                "city": "Portland",
                "state": "Oregon",
                "zip_code": "97201",
                "phone": "(503) 555-0303",
                "email": "contact@roosevelt.edu",
                "principal": "Jennifer Davis",
                "student_count": 680,
                "is_active": True
            },
            {
                "name": "Jefferson Academy",
                "address": "321 Pine Road",
                "city": "Austin",
                "state": "Texas",
                "zip_code": "73301",
                "phone": "(512) 555-0404",
                "email": "office@jefferson.edu",
                "principal": "Robert Martinez",
                "student_count": 890,
                "is_active": True
            }
        ]

        schools = []
        for school_data in schools_data:
            school = School(**school_data)
            session.add(school)
            schools.append(school)
        
        session.commit()

        # Create students
        students_data = [
            {
                "first_name": "Emma",
                "last_name": "Johnson",
                "email": "emma.johnson@email.com",
                "phone": "(217) 555-1001",
                "date_of_birth": date(2010, 3, 15),
                "grade_level": 8,
                "school_id": 1,
                "student_id_number": "LIN001",
                "enrollment_date": date(2023, 8, 15),
                "guardian_name": "Mary Johnson",
                "guardian_phone": "(217) 555-1000",
                "guardian_email": "mary.johnson@email.com",
                "address": "456 School Street",
                "city": "Springfield",
                "state": "Illinois",
                "zip_code": "62701",
                "is_active": True
            },
            {
                "first_name": "Liam",
                "last_name": "Chen",
                "email": "liam.chen@email.com",
                "phone": "(608) 555-2001",
                "date_of_birth": date(2006, 7, 22),
                "grade_level": 12,
                "school_id": 2,
                "student_id_number": "WAS002",
                "enrollment_date": date(2022, 8, 20),
                "guardian_name": "David Chen",
                "guardian_phone": "(608) 555-2000",
                "guardian_email": "david.chen@email.com",
                "address": "789 Student Avenue",
                "city": "Madison",
                "state": "Wisconsin",
                "zip_code": "53703",
                "is_active": True
            }
        ]

        students = []
        for student_data in students_data:
            student = Student(**student_data)
            session.add(student)
            students.append(student)
            
        session.commit()

        # Create invoices
        invoices_data = [
            {
                "invoice_number": "INV-2024-001",
                "student_id": 1,
                "school_id": 1,
                "amount": 850.00,
                "tax_amount": 68.00,
                "total_amount": 918.00,
                "description": "Tuition fee for Spring semester 2024",
                "invoice_date": date(2024, 1, 15),
                "due_date": date(2024, 2, 15),
                "payment_date": date(2024, 2, 10),
                "status": "paid",
                "payment_method": "bank_transfer",
                "created_at": datetime(2024, 1, 15, 9, 0, 0),
                "updated_at": datetime(2024, 2, 10, 14, 30, 0),
                "notes": "Payment received on time"
            },
            {
                "invoice_number": "INV-2024-002",
                "student_id": 2,
                "school_id": 2,
                "amount": 1200.00,
                "tax_amount": 96.00,
                "total_amount": 1296.00,
                "description": "High school tuition and laboratory fees",
                "invoice_date": date(2024, 1, 20),
                "due_date": date(2024, 2, 20),
                "payment_date": None,
                "status": "pending",
                "payment_method": None,
                "created_at": datetime(2024, 1, 20, 10, 0, 0),
                "updated_at": datetime(2024, 1, 20, 10, 0, 0),
                "notes": "Reminder sent on 2024-02-15"
            }
        ]

        for invoice_data in invoices_data:
            invoice = Invoice(**invoice_data)
            session.add(invoice)
            
        session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    from app.infrastructure.database.connection import create_db_and_tables
    create_db_and_tables()
    seed_data()
