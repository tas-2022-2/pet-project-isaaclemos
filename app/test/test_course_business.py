from unittest import mock

import pytest

from business.course_business import CourseBusiness
from model.course import Course
from service.course_service import CourseService


@pytest.fixture
def courses() -> list[Course]:
    return [Course(1, 'C# Design patterns',
                   'This course will help those students who are having knowledge of C# and visual studio',
                   3),
            Course(2, 'Angular 5',
                   'This course starts from scratch, you neither need to know Angular 1 nor Angular 2!',
                   27),
            Course(3, 'Java Master Class',
                   'Join just under 200,000 students just like you whoe having massive success with their Java',
                   72),
            Course(3, 'Java Spring MVC',
                   'How to program with spring MVC to the right way',
                   8)
            ]


def test_insert_course_into_list(courses):

    course = Course(id=1, name="Python", description="Lorem", total_hours=40)
    courses.append(course)
    assert len(courses) == 5


def test_size_list_courses_is_four(courses):
    # A lista de curso não deve ser alterada durante os testes
    assert len(courses) == 4


def test_filter_course_by_name_using_mock(courses):
    # Filtrando um curso por nome usando mock
    filter_count: int = 1
    course_service_mock = mock.Mock(spec=CourseService)
    course_service_mock.list_all_courses.return_value = courses

    course_business: CourseBusiness = CourseBusiness(course_service_mock)

    courses = course_business.filter_course_by_name("Spring")
    assert len(courses) == filter_count

# Criacção de um objeto stub para CourseService


class CourseServiceStub(CourseService):
    def __init__(self, courses: Course) -> None:
        self.courses = courses

    def list_all_courses(self) -> list[Course]:
        return self.courses

    def delete(self, course: Course) -> None:
        self.courses.remove(course)


def test_filter_course_by_name_using_stub(courses):
    # Filtrando um curso por nome usando stub
    filter_count = 2
    course_service_stub = CourseServiceStub(courses)
    course_business: CourseBusiness = CourseBusiness(course_service_stub)
    courses = course_business.filter_course_by_name("Java")

    assert len(courses) == filter_count


def test_delete_one_course(courses):
    # Removendo um curso da base para teste
    course_service_stub = CourseServiceStub(courses)
    course_business = CourseBusiness(course_service_stub)
    course_business.delete_course_by_name("Angular")

    assert len(courses) == 3
