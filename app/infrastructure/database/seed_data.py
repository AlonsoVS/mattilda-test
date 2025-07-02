from datetime import date, datetime
from sqlmodel import Session, select, text
from app.infrastructure.database.connection import engine
from app.infrastructure.persistence.school_entity import SchoolEntity
from app.infrastructure.persistence.student_entity import StudentEntity
from app.infrastructure.persistence.invoice_entity import InvoiceEntity
from app.domain.enums import InvoiceStatus, PaymentMethod
from app.infrastructure.database.migrations.create_users_table import CREATE_USERS_TABLE
from app.core.config import settings
from app.core.auth import get_password_hash
from app.domain.models.user import User
from app.infrastructure.repositories.user_repository import UserRepository


def create_users_table(session: Session):
    """Create users table if it doesn't exist"""
    try:
        # Execute raw SQL using execute()
        session.execute(text(CREATE_USERS_TABLE))
        session.commit()
        print("✅ Users table created successfully")
    except Exception as e:
        print(f"❌ Error creating users table: {e}")
        session.rollback()


async def create_default_admin_user(session: Session):
    """Create default admin user from environment configuration"""
    try:
        user_repository = UserRepository(session)
        
        # Check if admin user already exists
        existing_admin = await user_repository.get_by_username(settings.ADMIN_USERNAME)
        if existing_admin:
            print(f"✅ Admin user '{settings.ADMIN_USERNAME}' already exists")
            # Ensure existing user is a superuser
            if not existing_admin.is_superuser and existing_admin.id:
                await user_repository.update(existing_admin.id, {"is_superuser": True})
                print(f"✅ Updated '{settings.ADMIN_USERNAME}' to superuser")
            return existing_admin
        
        # Create new admin user
        print(f"Creating admin user '{settings.ADMIN_USERNAME}'...")
        hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        admin_user = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            full_name=settings.ADMIN_FULL_NAME,
            is_active=True,
            is_superuser=True
        )
        
        created_user = await user_repository.create(admin_user, hashed_password)
        print(f"✅ Admin user '{settings.ADMIN_USERNAME}' created successfully")
        print(f"   Email: {settings.ADMIN_EMAIL}")
        print(f"   Full Name: {settings.ADMIN_FULL_NAME}")
        
        return created_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        session.rollback()
        return None


async def seed_data():
    """Seed the database with initial data"""
    with Session(engine) as session:
        # Create users table first
        create_users_table(session)
        
        # Create default admin user
        await create_default_admin_user(session)
        
        # Check if data already exists
        existing_schools = session.exec(select(SchoolEntity)).first()
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
                "phone_number": "(217) 555-0101",
                "email": "info@lincoln.edu",
                "principal_name": "Sarah Johnson",
                "established_year": 1985,
                "is_active": True
            },
            {
                "name": "Washington High School",
                "address": "456 Oak Avenue",
                "city": "Madison",
                "state": "Wisconsin",
                "zip_code": "53703",
                "phone_number": "(608) 555-0202",
                "email": "admin@washington.edu",
                "principal_name": "Michael Chen",
                "established_year": 1963,
                "is_active": True
            },
            {
                "name": "Roosevelt Middle School",
                "address": "789 Elm Street",
                "city": "Portland",
                "state": "Oregon",
                "zip_code": "97201",
                "phone_number": "(503) 555-0303",
                "email": "contact@roosevelt.edu",
                "principal_name": "Jennifer Davis",
                "established_year": 1978,
                "is_active": True
            },
            {
                "name": "Jefferson Academy",
                "address": "321 Pine Road",
                "city": "Austin",
                "state": "Texas",
                "zip_code": "73301",
                "phone_number": "(512) 555-0404",
                "email": "office@jefferson.edu",
                "principal_name": "Robert Martinez",
                "established_year": 1992,
                "is_active": True
            },
            {
                "name": "Kennedy Elementary",
                "address": "555 Maple Drive",
                "city": "Denver",
                "state": "Colorado",
                "zip_code": "80201",
                "phone_number": "(303) 555-0505",
                "email": "info@kennedy.edu",
                "principal_name": "Lisa Thompson",
                "established_year": 1989,
                "is_active": True
            },
            {
                "name": "Franklin High School",
                "address": "777 Cedar Lane",
                "city": "Seattle",
                "state": "Washington",
                "zip_code": "98101",
                "phone_number": "(206) 555-0606",
                "email": "admin@franklin.edu",
                "principal_name": "David Wilson",
                "established_year": 1954,
                "is_active": True
            },
            {
                "name": "Adams Charter School",
                "address": "999 Birch Street",
                "city": "Phoenix",
                "state": "Arizona",
                "zip_code": "85001",
                "phone_number": "(602) 555-0707",
                "email": "contact@adams.edu",
                "principal_name": "Maria Rodriguez",
                "established_year": 2001,
                "is_active": True
            },
            {
                "name": "Hamilton Preparatory",
                "address": "1234 Walnut Avenue",
                "city": "Boston",
                "state": "Massachusetts",
                "zip_code": "02101",
                "phone_number": "(617) 555-0808",
                "email": "office@hamilton.edu",
                "principal_name": "James Brown",
                "established_year": 1875,
                "is_active": True
            },
            {
                "name": "Madison Elementary",
                "address": "567 Spruce Road",
                "city": "Atlanta",
                "state": "Georgia",
                "zip_code": "30301",
                "phone_number": "(404) 555-0909",
                "email": "info@madison.edu",
                "principal_name": "Patricia Garcia",
                "established_year": 1967,
                "is_active": True
            },
            {
                "name": "Monroe Middle School",
                "address": "890 Ash Boulevard",
                "city": "Miami",
                "state": "Florida",
                "zip_code": "33101",
                "phone_number": "(305) 555-1010",
                "email": "admin@monroe.edu",
                "principal_name": "Christopher Lee",
                "established_year": 1983,
                "is_active": True
            },
            {
                "name": "Inactive School (Closed)",
                "address": "999 Closed Street",
                "city": "Nowhere",
                "state": "Texas",
                "zip_code": "00000",
                "phone_number": "(000) 000-0000",
                "email": "closed@school.edu",
                "principal_name": "Former Principal",
                "established_year": 1950,
                "is_active": False
            }
        ]

        schools = []
        for school_data in schools_data:
            school = SchoolEntity(**school_data)
            session.add(school)
            schools.append(school)
        
        session.commit()

        # Create students
        students_data = [
            # Lincoln Elementary School (School ID 1) - Elementary students
            {
                "first_name": "Emma",
                "last_name": "Johnson",
                "email": "emma.johnson@email.com",
                "phone_number": "(217) 555-1001",
                "date_of_birth": date(2016, 3, 15),
                "grade_level": 2,
                "school_id": 1,
                "enrollment_date": date(2023, 8, 15),
                "address": "456 School Street",
                "is_active": True
            },
            {
                "first_name": "Noah",
                "last_name": "Williams",
                "email": "noah.williams@email.com",
                "phone_number": "(217) 555-1002",
                "date_of_birth": date(2015, 6, 8),
                "grade_level": 3,
                "school_id": 1,
                "enrollment_date": date(2022, 8, 20),
                "address": "789 Learning Lane",
                "is_active": True
            },
            {
                "first_name": "Olivia",
                "last_name": "Brown",
                "email": "olivia.brown@email.com",
                "phone_number": "(217) 555-1003",
                "date_of_birth": date(2014, 11, 25),
                "grade_level": 4,
                "school_id": 1,
                "enrollment_date": date(2021, 8, 18),
                "address": "321 Education Blvd",
                "is_active": True
            },
            {
                "first_name": "Lucas",
                "last_name": "Davis",
                "email": "lucas.davis@email.com",
                "phone_number": "(217) 555-1004",
                "date_of_birth": date(2013, 4, 12),
                "grade_level": 5,
                "school_id": 1,
                "enrollment_date": date(2020, 8, 25),
                "address": "654 Knowledge Ave",
                "is_active": True
            },
            
            # Washington High School (School ID 2) - High school students
            {
                "first_name": "Liam",
                "last_name": "Chen",
                "email": "liam.chen@email.com",
                "phone_number": "(608) 555-2001",
                "date_of_birth": date(2006, 7, 22),
                "grade_level": 12,
                "school_id": 2,
                "enrollment_date": date(2022, 8, 20),
                "address": "789 Student Avenue",
                "is_active": True
            },
            {
                "first_name": "Sophia",
                "last_name": "Martinez",
                "email": "sophia.martinez@email.com",
                "phone_number": "(608) 555-2002",
                "date_of_birth": date(2007, 2, 14),
                "grade_level": 11,
                "school_id": 2,
                "enrollment_date": date(2023, 8, 22),
                "address": "123 Academic Road",
                "is_active": True
            },
            {
                "first_name": "Mason",
                "last_name": "Anderson",
                "email": "mason.anderson@email.com",
                "phone_number": "(608) 555-2003",
                "date_of_birth": date(2008, 9, 3),
                "grade_level": 10,
                "school_id": 2,
                "enrollment_date": date(2024, 8, 19),
                "address": "456 Scholar Street",
                "is_active": True
            },
            {
                "first_name": "Isabella",
                "last_name": "Taylor",
                "email": "isabella.taylor@email.com",
                "phone_number": "(608) 555-2004",
                "date_of_birth": date(2009, 12, 17),
                "grade_level": 9,
                "school_id": 2,
                "enrollment_date": date(2024, 8, 21),
                "address": "789 Campus Circle",
                "is_active": True
            },
            
            # Roosevelt Middle School (School ID 3) - Middle school students
            {
                "first_name": "Ethan",
                "last_name": "Thompson",
                "email": "ethan.thompson@email.com",
                "phone_number": "(503) 555-3001",
                "date_of_birth": date(2011, 5, 30),
                "grade_level": 7,
                "school_id": 3,
                "enrollment_date": date(2023, 8, 17),
                "address": "111 Middle Way",
                "is_active": True
            },
            {
                "first_name": "Mia",
                "last_name": "Garcia",
                "email": "mia.garcia@email.com",
                "phone_number": "(503) 555-3002",
                "date_of_birth": date(2010, 8, 7),
                "grade_level": 8,
                "school_id": 3,
                "enrollment_date": date(2022, 8, 16),
                "address": "222 Junior Lane",
                "is_active": True
            },
            {
                "first_name": "Alexander",
                "last_name": "Wilson",
                "email": "alexander.wilson@email.com",
                "phone_number": "(503) 555-3003",
                "date_of_birth": date(2012, 1, 19),
                "grade_level": 6,
                "school_id": 3,
                "enrollment_date": date(2024, 8, 20),
                "address": "333 Tween Terrace",
                "is_active": True
            },
            
            # Jefferson Academy (School ID 4) - Mixed grades
            {
                "first_name": "Charlotte",
                "last_name": "Moore",
                "email": "charlotte.moore@email.com",
                "phone_number": "(512) 555-4001",
                "date_of_birth": date(2007, 10, 11),
                "grade_level": 11,
                "school_id": 4,
                "enrollment_date": date(2023, 8, 15),
                "address": "444 Academy Ave",
                "is_active": True
            },
            {
                "first_name": "James",
                "last_name": "Jackson",
                "email": "james.jackson@email.com",
                "phone_number": "(512) 555-4002",
                "date_of_birth": date(2008, 3, 28),
                "grade_level": 10,
                "school_id": 4,
                "enrollment_date": date(2024, 8, 18),
                "address": "555 Prep Place",
                "is_active": True
            },
            
            # Kennedy Elementary (School ID 5) - Elementary students
            {
                "first_name": "Amelia",
                "last_name": "White",
                "email": "amelia.white@email.com",
                "phone_number": "(303) 555-5001",
                "date_of_birth": date(2015, 7, 5),
                "grade_level": 3,
                "school_id": 5,
                "enrollment_date": date(2022, 8, 22),
                "address": "666 Elementary East",
                "is_active": True
            },
            {
                "first_name": "Benjamin",
                "last_name": "Harris",
                "email": "benjamin.harris@email.com",
                "phone_number": "(303) 555-5002",
                "date_of_birth": date(2014, 12, 3),
                "grade_level": 4,
                "school_id": 5,
                "enrollment_date": date(2021, 8, 19),
                "address": "777 Primary Path",
                "is_active": True
            },
            
            # Franklin High School (School ID 6) - High school students
            {
                "first_name": "Harper",
                "last_name": "Clark",
                "email": "harper.clark@email.com",
                "phone_number": "(206) 555-6001",
                "date_of_birth": date(2006, 4, 16),
                "grade_level": 12,
                "school_id": 6,
                "enrollment_date": date(2022, 8, 17),
                "address": "888 Senior Street",
                "is_active": True
            },
            {
                "first_name": "Elijah",
                "last_name": "Lewis",
                "email": "elijah.lewis@email.com",
                "phone_number": "(206) 555-6002",
                "date_of_birth": date(2007, 11, 9),
                "grade_level": 11,
                "school_id": 6,
                "enrollment_date": date(2023, 8, 21),
                "address": "999 Franklin Way",
                "is_active": True
            },
            
            # Adams Charter School (School ID 7) - Mixed grades
            {
                "first_name": "Evelyn",
                "last_name": "Young",
                "email": "evelyn.young@email.com",
                "phone_number": "(602) 555-7001",
                "date_of_birth": date(2010, 6, 23),
                "grade_level": 8,
                "school_id": 7,
                "enrollment_date": date(2022, 8, 24),
                "address": "101 Charter Circle",
                "is_active": True
            },
            {
                "first_name": "William",
                "last_name": "King",
                "email": "william.king@email.com",
                "phone_number": "(602) 555-7002",
                "date_of_birth": date(2011, 9, 12),
                "grade_level": 7,
                "school_id": 7,
                "enrollment_date": date(2023, 8, 23),
                "address": "202 Innovation Ave",
                "is_active": True
            },
            
            # Hamilton Preparatory (School ID 8) - Prep school students
            {
                "first_name": "Abigail",
                "last_name": "Wright",
                "email": "abigail.wright@email.com",
                "phone_number": "(617) 555-8001",
                "date_of_birth": date(2006, 1, 8),
                "grade_level": 12,
                "school_id": 8,
                "enrollment_date": date(2022, 8, 16),
                "address": "303 Prep Plaza",
                "is_active": True
            },
            {
                "first_name": "Henry",
                "last_name": "Lopez",
                "email": "henry.lopez@email.com",
                "phone_number": "(617) 555-8002",
                "date_of_birth": date(2007, 8, 21),
                "grade_level": 11,
                "school_id": 8,
                "enrollment_date": date(2023, 8, 18),
                "address": "404 Elite Elm",
                "is_active": True
            },
            
            # Madison Elementary (School ID 9) - Elementary students
            {
                "first_name": "Emily",
                "last_name": "Hill",
                "email": "emily.hill@email.com",
                "phone_number": "(404) 555-9001",
                "date_of_birth": date(2016, 2, 29),
                "grade_level": 2,
                "school_id": 9,
                "enrollment_date": date(2023, 8, 20),
                "address": "505 Little Lane",
                "is_active": True
            },
            {
                "first_name": "Michael",
                "last_name": "Green",
                "email": "michael.green@email.com",
                "phone_number": "(404) 555-9002",
                "date_of_birth": date(2015, 5, 14),
                "grade_level": 3,
                "school_id": 9,
                "enrollment_date": date(2022, 8, 17),
                "address": "606 Madison Manor",
                "is_active": True
            },
            
            # Monroe Middle School (School ID 10) - Middle school students
            {
                "first_name": "Elizabeth",
                "last_name": "Adams",
                "email": "elizabeth.adams@email.com",
                "phone_number": "(305) 555-1001",
                "date_of_birth": date(2011, 10, 6),
                "grade_level": 7,
                "school_id": 10,
                "enrollment_date": date(2023, 8, 19),
                "address": "707 Middle Miami",
                "is_active": True
            },
            {
                "first_name": "Daniel",
                "last_name": "Baker",
                "email": "daniel.baker@email.com",
                "phone_number": "(305) 555-1002",
                "date_of_birth": date(2010, 12, 27),
                "grade_level": 8,
                "school_id": 10,
                "enrollment_date": date(2022, 8, 21),
                "address": "808 Monroe Mile",
                "is_active": True
            },
            
            # Inactive student for testing
            {
                "first_name": "Inactive",
                "last_name": "Student",
                "email": "inactive.student@email.com",
                "phone_number": "(000) 000-0000",
                "date_of_birth": date(2010, 1, 1),
                "grade_level": 8,
                "school_id": 3,
                "enrollment_date": date(2022, 8, 15),
                "address": "999 Withdrawn Way",
                "is_active": False
            }
        ]

        students = []
        for student_data in students_data:
            student = StudentEntity(**student_data)
            session.add(student)
            students.append(student)
            
        session.commit()

        # Create invoices
        invoices_data = [
            # Paid invoices
            {
                "invoice_number": "INV-2024-001",
                "student_id": 1,
                "school_id": 1,
                "amount": 850.00,
                "tax_amount": 68.00,
                "total_amount": 918.00,
                "description": "Elementary tuition fee for Spring semester 2024",
                "invoice_date": date(2024, 1, 15),
                "due_date": date(2024, 2, 15),
                "payment_date": date(2024, 2, 10),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.BANK_TRANSFER,
                "created_at": datetime(2024, 1, 15, 9, 0, 0),
                "updated_at": datetime(2024, 2, 10, 14, 30, 0),
                "notes": "Payment received on time"
            },
            {
                "invoice_number": "INV-2024-002",
                "student_id": 5,
                "school_id": 2,
                "amount": 1200.00,
                "tax_amount": 96.00,
                "total_amount": 1296.00,
                "description": "High school tuition and laboratory fees",
                "invoice_date": date(2024, 1, 20),
                "due_date": date(2024, 2, 20),
                "payment_date": date(2024, 2, 18),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CREDIT_CARD,
                "created_at": datetime(2024, 1, 20, 10, 0, 0),
                "updated_at": datetime(2024, 2, 18, 16, 45, 0),
                "notes": "Paid via online portal"
            },
            {
                "invoice_number": "INV-2024-003",
                "student_id": 9,
                "school_id": 3,
                "amount": 950.00,
                "tax_amount": 76.00,
                "total_amount": 1026.00,
                "description": "Middle school tuition and activity fees",
                "invoice_date": date(2024, 2, 1),
                "due_date": date(2024, 3, 1),
                "payment_date": date(2024, 2, 25),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CHECK,
                "created_at": datetime(2024, 2, 1, 8, 30, 0),
                "updated_at": datetime(2024, 2, 25, 11, 15, 0),
                "notes": "Check payment processed"
            },
            
            # Pending invoices
            {
                "invoice_number": "INV-2024-004",
                "student_id": 11,
                "school_id": 4,
                "amount": 1500.00,
                "tax_amount": 120.00,
                "total_amount": 1620.00,
                "description": "Academy premium tuition and materials",
                "invoice_date": date(2024, 2, 15),
                "due_date": date(2024, 3, 15),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 15, 9, 0, 0),
                "updated_at": datetime(2024, 2, 15, 9, 0, 0),
                "notes": "First reminder sent"
            },
            {
                "invoice_number": "INV-2024-005",
                "student_id": 13,
                "school_id": 5,
                "amount": 750.00,
                "tax_amount": 60.00,
                "total_amount": 810.00,
                "description": "Elementary tuition and supplies",
                "invoice_date": date(2024, 2, 20),
                "due_date": date(2024, 3, 20),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 20, 10, 30, 0),
                "updated_at": datetime(2024, 2, 20, 10, 30, 0),
                "notes": "Recently issued"
            },
            
            # Overdue invoices
            {
                "invoice_number": "INV-2024-006",
                "student_id": 15,
                "school_id": 6,
                "amount": 1300.00,
                "tax_amount": 104.00,
                "total_amount": 1404.00,
                "description": "High school tuition - Fall semester",
                "invoice_date": date(2023, 12, 1),
                "due_date": date(2024, 1, 1),
                "payment_date": None,
                "status": InvoiceStatus.OVERDUE,
                "payment_method": None,
                "created_at": datetime(2023, 12, 1, 9, 0, 0),
                "updated_at": datetime(2024, 1, 15, 14, 0, 0),
                "notes": "Multiple reminders sent - final notice issued"
            },
            {
                "invoice_number": "INV-2024-007",
                "student_id": 17,
                "school_id": 7,
                "amount": 1100.00,
                "tax_amount": 88.00,
                "total_amount": 1188.00,
                "description": "Charter school tuition and technology fee",
                "invoice_date": date(2023, 11, 15),
                "due_date": date(2023, 12, 15),
                "payment_date": None,
                "status": InvoiceStatus.OVERDUE,
                "payment_method": None,
                "created_at": datetime(2023, 11, 15, 11, 0, 0),
                "updated_at": datetime(2024, 1, 10, 16, 30, 0),
                "notes": "Account under review - payment plan needed"
            },
            
            # Cancelled invoices
            {
                "invoice_number": "INV-2024-008",
                "student_id": 19,
                "school_id": 8,
                "amount": 2000.00,
                "tax_amount": 160.00,
                "total_amount": 2160.00,
                "description": "Preparatory school premium program",
                "invoice_date": date(2024, 1, 10),
                "due_date": date(2024, 2, 10),
                "payment_date": None,
                "status": InvoiceStatus.CANCELLED,
                "payment_method": None,
                "created_at": datetime(2024, 1, 10, 9, 0, 0),
                "updated_at": datetime(2024, 1, 25, 13, 45, 0),
                "notes": "Student transferred to different program"
            },
            
            # More paid invoices with different payment methods
            {
                "invoice_number": "INV-2024-009",
                "student_id": 2,
                "school_id": 1,
                "amount": 825.00,
                "tax_amount": 66.00,
                "total_amount": 891.00,
                "description": "Elementary tuition - Winter term",
                "invoice_date": date(2024, 2, 5),
                "due_date": date(2024, 3, 5),
                "payment_date": date(2024, 3, 1),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CASH,
                "created_at": datetime(2024, 2, 5, 8, 0, 0),
                "updated_at": datetime(2024, 3, 1, 10, 0, 0),
                "notes": "Cash payment received at office"
            },
            {
                "invoice_number": "INV-2024-010",
                "student_id": 6,
                "school_id": 2,
                "amount": 1250.00,
                "tax_amount": 100.00,
                "total_amount": 1350.00,
                "description": "High school advanced placement fees",
                "invoice_date": date(2024, 1, 30),
                "due_date": date(2024, 2, 28),
                "payment_date": date(2024, 2, 15),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.BANK_TRANSFER,
                "created_at": datetime(2024, 1, 30, 14, 0, 0),
                "updated_at": datetime(2024, 2, 15, 12, 30, 0),
                "notes": "Early payment discount applied"
            },
            
            # More diverse invoices
            {
                "invoice_number": "INV-2024-011",
                "student_id": 10,
                "school_id": 3,
                "amount": 500.00,
                "tax_amount": 40.00,
                "total_amount": 540.00,
                "description": "Middle school sports program fee",
                "invoice_date": date(2024, 2, 10),
                "due_date": date(2024, 3, 10),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 10, 9, 30, 0),
                "updated_at": datetime(2024, 2, 10, 9, 30, 0),
                "notes": "Sports equipment and coaching fees"
            },
            {
                "invoice_number": "INV-2024-012",
                "student_id": 21,
                "school_id": 9,
                "amount": 300.00,
                "tax_amount": 24.00,
                "total_amount": 324.00,
                "description": "Elementary art supplies and materials",
                "invoice_date": date(2024, 2, 12),
                "due_date": date(2024, 3, 12),
                "payment_date": date(2024, 2, 28),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CREDIT_CARD,
                "created_at": datetime(2024, 2, 12, 11, 0, 0),
                "updated_at": datetime(2024, 2, 28, 15, 20, 0),
                "notes": "Art program supplemental fee"
            },
            {
                "invoice_number": "INV-2024-013",
                "student_id": 23,
                "school_id": 10,
                "amount": 675.00,
                "tax_amount": 54.00,
                "total_amount": 729.00,
                "description": "Middle school science lab fee",
                "invoice_date": date(2024, 1, 25),
                "due_date": date(2024, 2, 25),
                "payment_date": None,
                "status": InvoiceStatus.OVERDUE,
                "payment_method": None,
                "created_at": datetime(2024, 1, 25, 13, 0, 0),
                "updated_at": datetime(2024, 3, 1, 9, 0, 0),
                "notes": "Lab equipment and experiment materials"
            },
            
            # Partial payment scenarios
            {
                "invoice_number": "INV-2024-014",
                "student_id": 12,
                "school_id": 4,
                "amount": 1800.00,
                "tax_amount": 144.00,
                "total_amount": 1944.00,
                "description": "Academy full semester tuition",
                "invoice_date": date(2024, 1, 5),
                "due_date": date(2024, 2, 5),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 1, 5, 8, 0, 0),
                "updated_at": datetime(2024, 2, 10, 10, 0, 0),
                "notes": "Payment plan requested - installments arranged"
            },
            {
                "invoice_number": "INV-2024-015",
                "student_id": 16,
                "school_id": 6,
                "amount": 450.00,
                "tax_amount": 36.00,
                "total_amount": 486.00,
                "description": "High school graduation ceremony fee",
                "invoice_date": date(2024, 2, 14),
                "due_date": date(2024, 3, 14),
                "payment_date": date(2024, 3, 10),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CHECK,
                "created_at": datetime(2024, 2, 14, 10, 0, 0),
                "updated_at": datetime(2024, 3, 10, 14, 0, 0),
                "notes": "Senior year graduation package"
            },
            
            # Scholarship and financial aid invoices
            {
                "invoice_number": "INV-2024-016",
                "student_id": 20,
                "school_id": 8,
                "amount": 1200.00,
                "tax_amount": 96.00,
                "total_amount": 1296.00,
                "description": "Preparatory school tuition (scholarship applied)",
                "invoice_date": date(2024, 2, 1),
                "due_date": date(2024, 3, 1),
                "payment_date": date(2024, 2, 20),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.BANK_TRANSFER,
                "created_at": datetime(2024, 2, 1, 9, 0, 0),
                "updated_at": datetime(2024, 2, 20, 11, 30, 0),
                "notes": "50% scholarship discount applied"
            },
            
            # Technology and special program fees
            {
                "invoice_number": "INV-2024-017",
                "student_id": 18,
                "school_id": 7,
                "amount": 250.00,
                "tax_amount": 20.00,
                "total_amount": 270.00,
                "description": "Charter school technology upgrade fee",
                "invoice_date": date(2024, 2, 8),
                "due_date": date(2024, 3, 8),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 8, 12, 0, 0),
                "updated_at": datetime(2024, 2, 8, 12, 0, 0),
                "notes": "New tablet and software licensing"
            },
            {
                "invoice_number": "INV-2024-018",
                "student_id": 14,
                "school_id": 5,
                "amount": 180.00,
                "tax_amount": 14.40,
                "total_amount": 194.40,
                "description": "Elementary music program fee",
                "invoice_date": date(2024, 2, 18),
                "due_date": date(2024, 3, 18),
                "payment_date": date(2024, 3, 5),
                "status": InvoiceStatus.PAID,
                "payment_method": PaymentMethod.CREDIT_CARD,
                "created_at": datetime(2024, 2, 18, 15, 0, 0),
                "updated_at": datetime(2024, 3, 5, 9, 45, 0),
                "notes": "Instrument rental and lesson fees"
            },
            
            # Summer program invoices
            {
                "invoice_number": "INV-2024-019",
                "student_id": 22,
                "school_id": 9,
                "amount": 600.00,
                "tax_amount": 48.00,
                "total_amount": 648.00,
                "description": "Summer enrichment program",
                "invoice_date": date(2024, 2, 25),
                "due_date": date(2024, 3, 25),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 25, 10, 0, 0),
                "updated_at": datetime(2024, 2, 25, 10, 0, 0),
                "notes": "June-July summer camp and activities"
            },
            {
                "invoice_number": "INV-2024-020",
                "student_id": 24,
                "school_id": 10,
                "amount": 880.00,
                "tax_amount": 70.40,
                "total_amount": 950.40,
                "description": "Summer STEM academy program",
                "invoice_date": date(2024, 2, 22),
                "due_date": date(2024, 3, 22),
                "payment_date": None,
                "status": InvoiceStatus.PENDING,
                "payment_method": None,
                "created_at": datetime(2024, 2, 22, 14, 30, 0),
                "updated_at": datetime(2024, 2, 22, 14, 30, 0),
                "notes": "Advanced robotics and coding bootcamp"
            }
        ]

        for invoice_data in invoices_data:
            invoice = InvoiceEntity(**invoice_data)
            session.add(invoice)
            
        session.commit()

        print("✅ Database seeded successfully!")
        print(f"   📚 Created {len(schools_data)} schools")
        print(f"   👥 Created {len(students_data)} students") 
        print(f"   📄 Created {len(invoices_data)} invoices")
        print("   🎯 Data includes various statuses and scenarios:")
        print("      - Schools: Active and inactive institutions")
        print("      - Students: All grade levels (K-12) across different schools")
        print("      - Invoices: Paid, pending, overdue, and cancelled statuses")
        print("      - Payment methods: Bank transfer, credit card, check, cash")
        print("      - Diverse scenarios: Scholarships, payment plans, special programs")


def seed_data_sync():
    """Synchronous wrapper for seed_data function"""
    import asyncio
    asyncio.run(seed_data())


if __name__ == "__main__":
    import asyncio
    from app.infrastructure.database.connection import create_db_and_tables
    
    create_db_and_tables()
    asyncio.run(seed_data())
