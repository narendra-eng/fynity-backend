from app.extensions import db
from app.models.mentorship_student import MentorshipStudent


def create_mentorship_student(
    full_name: str,
    email: str,
    phone: str,
    college: str,
    course: str,
    year: int
) -> dict:

    existing_student = MentorshipStudent.query.filter_by(email=email).first()

    if existing_student:
        return {
            "success": False,
            "message": "Mentorship student already exists."
        }

    student = MentorshipStudent(
        full_name=full_name,
        email=email,
        phone=phone,
        college=college,
        course=course,
        year=year
    )

    try:
        db.session.add(student)
        db.session.commit()

        return {
            "success": True,
            "message": "Mentorship student created successfully.",
            "mentorship_student": student.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create mentorship student."
        }


def get_all_mentorship_students() -> dict:

    students = MentorshipStudent.query.all()

    return {
        "success": True,
        "count": len(students),
        "mentorship_students": [
            student.to_dict() for student in students
        ]
    }


def get_mentorship_student_by_id(student_id: str) -> dict:

    student = MentorshipStudent.query.get(student_id)

    if not student:
        return {
            "success": False,
            "message": "Mentorship student not found."
        }

    return {
        "success": True,
        "mentorship_student": student.to_dict()
    }


def update_mentorship_student(
    student_id: str,
    data: dict
) -> dict:

    student = MentorshipStudent.query.get(student_id)

    if not student:
        return {
            "success": False,
            "message": "Mentorship student not found."
        }

    if "full_name" in data:
        student.full_name = data["full_name"]

    if "email" in data:
        student.email = data["email"]

    if "phone" in data:
        student.phone = data["phone"]

    if "college" in data:
        student.college = data["college"]

    if "course" in data:
        student.course = data["course"]

    if "year" in data:
        student.year = data["year"]

    if "status" in data:
        student.status = data["status"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Mentorship student updated successfully.",
            "mentorship_student": student.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update mentorship student."
        }


def delete_mentorship_student(student_id: str) -> dict:

    student = MentorshipStudent.query.get(student_id)

    if not student:
        return {
            "success": False,
            "message": "Mentorship student not found."
        }

    try:
        db.session.delete(student)
        db.session.commit()

        return {
            "success": True,
            "message": "Mentorship student deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete mentorship student."
        }