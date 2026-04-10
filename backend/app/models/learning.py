"""
Finvee Backend - Learning Models
Course, Student, Progress, and Tutoring
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import uuid
import json


def generate_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


@dataclass
class Course:
    course_id: str
    user_id: str  # creator/teacher
    title: str
    description: str
    category: str  # math, science, language, etc.
    difficulty: str  # beginner, intermediate, advanced
    duration_hours: float
    modules: List[Dict[str, Any]]  # lesson structure
    is_published: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "duration_hours": self.duration_hours,
            "modules": self.modules,
            "is_published": self.is_published,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class Enrollment:
    enrollment_id: str
    course_id: str
    student_id: str
    status: str  # enrolled, in_progress, completed
    progress_percent: float = 0.0
    enrolled_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "course_id": self.course_id,
            "student_id": self.student_id,
            "status": self.status,
            "progress_percent": self.progress_percent,
            "enrolled_at": self.enrolled_at,
            "completed_at": self.completed_at,
        }


@dataclass
class LessonProgress:
    progress_id: str
    enrollment_id: str
    lesson_id: str
    completed: bool = False
    time_spent_minutes: int = 0
    quiz_score: Optional[float] = None
    completed_at: Optional[str] = None

    def to_dict(self):
        return {
            "progress_id": self.progress_id,
            "enrollment_id": self.enrollment_id,
            "lesson_id": self.lesson_id,
            "completed": self.completed,
            "time_spent_minutes": self.time_spent_minutes,
            "quiz_score": self.quiz_score,
            "completed_at": self.completed_at,
        }


@dataclass
class TutoringSession:
    session_id: str
    student_id: str
    course_id: Optional[str]
    topic: str
    messages: List[Dict[str, Any]]  # chat history
    status: str  # active, completed
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "topic": self.topic,
            "messages": self.messages,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class LearningPath:
    path_id: str
    user_id: str
    title: str
    recommended_courses: List[str]  # course_ids
    current_course_index: int = 0
    estimated_hours: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return {
            "path_id": self.path_id,
            "user_id": self.user_id,
            "title": self.title,
            "recommended_courses": self.recommended_courses,
            "current_course_index": self.current_course_index,
            "estimated_hours": self.estimated_hours,
            "created_at": self.created_at,
        }


class LearningManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {
                "courses": {},
                "enrollments": {},
                "progress": {},
                "sessions": {},
                "paths": {},
            }
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        import os

        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        data_file = os.path.join(data_dir, "learning.json")

        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                self._data = json.load(f)

    def _save_data(self):
        import os

        data_dir = os.path.join(os.path.dirname(__file__), "../../data")
        os.makedirs(data_dir, exist_ok=True)
        data_file = os.path.join(data_dir, "learning.json")

        with open(data_file, "w") as f:
            json.dump(self._data, f, indent=2)

    def create_course(
        self,
        user_id: str,
        title: str,
        description: str,
        category: str,
        difficulty: str,
        duration_hours: float,
        modules: List[Dict[str, Any]],
    ) -> Course:
        course = Course(
            course_id=generate_id("crs_"),
            user_id=user_id,
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            duration_hours=duration_hours,
            modules=modules,
        )
        self._data["courses"][course.course_id] = course.to_dict()
        self._save_data()
        return course

    def get_courses(
        self,
        user_id: str = None,
        category: str = None,
        difficulty: str = None,
        published_only: bool = True,
    ) -> List[Course]:
        courses = [Course(**c) for c in self._data["courses"].values()]

        if user_id:
            courses = [c for c in courses if c.user_id == user_id]
        if category:
            courses = [c for c in courses if c.category == category]
        if difficulty:
            courses = [c for c in courses if c.difficulty == difficulty]
        if published_only:
            courses = [c for c in courses if c.is_published]

        return courses

    def update_course(self, course_id: str, **kwargs):
        if course_id in self._data["courses"]:
            self._data["courses"][course_id].update(kwargs)
            self._data["courses"][course_id]["updated_at"] = datetime.now().isoformat()
            self._save_data()

    def enroll_student(self, course_id: str, student_id: str) -> Enrollment:
        enrollment = Enrollment(
            enrollment_id=generate_id("enr_"),
            course_id=course_id,
            student_id=student_id,
            status="enrolled",
        )
        self._data["enrollments"][enrollment.enrollment_id] = enrollment.to_dict()
        self._save_data()
        return enrollment

    def get_enrollments(
        self, student_id: str = None, course_id: str = None
    ) -> List[Enrollment]:
        enrollments = [Enrollment(**e) for e in self._data["enrollments"].values()]

        if student_id:
            enrollments = [e for e in enrollments if e.student_id == student_id]
        if course_id:
            enrollments = [e for e in enrollments if e.course_id == course_id]

        return enrollments

    def update_progress(
        self,
        enrollment_id: str,
        lesson_id: str,
        completed: bool = False,
        time_spent: int = 0,
        quiz_score: float = None,
    ):
        progress_id = f"{enrollment_id}_{lesson_id}"

        progress = LessonProgress(
            progress_id=progress_id,
            enrollment_id=enrollment_id,
            lesson_id=lesson_id,
            completed=completed,
            time_spent_minutes=time_spent,
            quiz_score=quiz_score,
            completed_at=datetime.now().isoformat() if completed else None,
        )

        self._data["progress"][progress_id] = progress.to_dict()

        # Update enrollment progress
        enrollment = self._data["enrollments"].get(enrollment_id)
        if enrollment:
            all_progress = [
                p
                for p in self._data["progress"].values()
                if p["enrollment_id"] == enrollment_id
            ]
            completed_count = sum(1 for p in all_progress if p["completed"])
            # Get total lessons from course
            course = self._data["courses"].get(enrollment["course_id"])
            total_lessons = len(course["modules"]) if course else 1
            enrollment["progress_percent"] = (
                (completed_count / total_lessons * 100) if total_lessons > 0 else 0
            )

            if enrollment["progress_percent"] >= 100:
                enrollment["status"] = "completed"
                enrollment["completed_at"] = datetime.now().isoformat()
            elif enrollment["progress_percent"] > 0:
                enrollment["status"] = "in_progress"

        self._save_data()

    def create_tutoring_session(
        self, student_id: str, course_id: str = None, topic: str = ""
    ) -> TutoringSession:
        session = TutoringSession(
            session_id=generate_id("tut_"),
            student_id=student_id,
            course_id=course_id,
            topic=topic,
            messages=[],
            status="active",
        )
        self._data["sessions"][session.session_id] = session.to_dict()
        self._save_data()
        return session

    def add_message(self, session_id: str, role: str, content: str):
        if session_id in self._data["sessions"]:
            self._data["sessions"][session_id]["messages"].append(
                {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            self._data["sessions"][session_id]["updated_at"] = (
                datetime.now().isoformat()
            )
            self._save_data()

    def get_sessions(
        self, student_id: str = None, status: str = None
    ) -> List[TutoringSession]:
        sessions = [TutoringSession(**s) for s in self._data["sessions"].values()]

        if student_id:
            sessions = [s for s in sessions if s.student_id == student_id]
        if status:
            sessions = [s for s in sessions if s.status == status]

        return sessions

    def generate_learning_path(
        self, user_id: str, title: str, course_ids: List[str]
    ) -> LearningPath:
        total_hours = 0
        for cid in course_ids:
            course = self._data["courses"].get(cid)
            if course:
                total_hours += course.get("duration_hours", 0)

        path = LearningPath(
            path_id=generate_id("lpn_"),
            user_id=user_id,
            title=title,
            recommended_courses=course_ids,
            estimated_hours=total_hours,
        )
        self._data["paths"][path.path_id] = path.to_dict()
        self._save_data()
        return path

    def get_learning_paths(self, user_id: str) -> List[LearningPath]:
        return [
            LearningPath(**p)
            for p in self._data["paths"].values()
            if p["user_id"] == user_id
        ]
