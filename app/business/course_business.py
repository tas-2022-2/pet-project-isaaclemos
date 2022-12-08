from service.course_service import CourseService
from model.course import Course


class CourseBusiness:

    def __init__(self, course_service: CourseService):
        self.course_service = course_service

    def filter_course_by_name(self, name: str) -> list[Course]:

        courses: list[Course] = self.course_service.list_all_courses()
        filtered_courses: list[Course] = list()

        for course in courses:
            if course.name.__contains__(name):
                filtered_courses.append(course)

        return filtered_courses

    def delete_course_by_name(self, name: str) -> None:

        courses = self.course_service.list_all_courses()

        for course in courses:
            if course.name.__contains__(name):
                self.course_service.delete(course)
