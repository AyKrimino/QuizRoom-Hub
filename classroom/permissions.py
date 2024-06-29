from rest_framework.permissions import BasePermission

from account.models import StudentProfile, TeacherProfile
from classroom.models import StudentClassroom


class IsClassroomMember(BasePermission):
    """
    Permission class to check if a user is a member of a classroom.

    The user is granted permission if:
    1. The user is the teacher who created the classroom.
    2. The user is a student who is a member of the classroom.

    This class assumes the presence of the following models:
    - `Classroom`: A model representing a classroom, with a foreign key to the teacher.
    - `StudentProfile`: A model representing the profile of a student, with a one-to-one link to the user.
    - `StudentClassroom`: A model representing the many-to-many relationship between students and classrooms.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user has permission to access the classroom object.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.
            obj: The classroom object that is being accessed.

        Returns:
            bool: True if the user is the teacher who created the classroom or a student member of the classroom,
                  False otherwise.
        """
        # Check if the user is the teacher who created the classroom
        if obj.teacher.user == request.user:
            return True

        # Check if the user is a student in the classroom
        try:
            # Retrieve the student's profile based on the user
            student = StudentProfile.objects.get(user=request.user)
            # Check if the student is enrolled in the classroom
            return StudentClassroom.objects.filter(classroom=obj, student=student).exists()
        except StudentProfile.DoesNotExist:
            # If the student's profile does not exist, the user is not a student
            return False


class IsClassroomOwner(BasePermission):
    """
    Permission class to check if a user is the owner of a classroom.

    The user is granted permission if they are the teacher who created the classroom.

    This class assumes the presence of the following model:
    - `Classroom`: A model representing a classroom, with a foreign key to the teacher.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user has permission to access the classroom object.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.
            obj: The classroom object that is being accessed.

        Returns:
            bool: True if the user is the teacher who created the classroom,
                  False otherwise.
        """
        # Check if the user is the teacher who created the classroom
        return request.user == obj.teacher.user


class IsStudent(BasePermission):
    """
    Permission class to check if a user is a student.

    The user is granted permission if they have a corresponding `StudentProfile`.

    This class assumes the presence of the following model:
    - `StudentProfile`: A model representing the profile of a student, with a one-to-one link to the user.
    """

    def has_permission(self, request, view):
        """
        Check if the request user has permission to access the view as a student.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.
        Returns:
            bool: True if the user has a `StudentProfile`, False otherwise.
        """
        # Check if the user has a StudentProfile
        return StudentProfile.objects.filter(user=request.user).exists()


class IsTeacher(BasePermission):
    """
    Permission class to check if a user is a teacher.

    The user is granted permission if they have a corresponding `TeacherProfile`.

    This class assumes the presence of the following model:
    - `TeacherProfile`: A model representing the profile of a teacher, with a one-to-one link to the user.
    """

    def has_permission(self, request, view):
        """
        Check if the request user has permission to access the view as a teacher.

        Args:
            request: The HTTP request object.
            view: The view that is being accessed.

        Returns:
            bool: True if the user has a `TeacherProfile`, False otherwise.
        """
        # Check if the user has a TeacherProfile
        return TeacherProfile.objects.filter(user=request.user).exists()


IsStudentOrTeacher = IsStudent | IsTeacher
