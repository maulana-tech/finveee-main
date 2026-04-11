"""
Finvee Backend - Learning API Routes
"""

from flask import request, jsonify, Blueprint
import traceback

learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/courses", methods=["GET"])
def get_courses():
    """Get courses with optional filters"""
    try:
        user_id = request.headers.get("X-User-ID")
        category = request.args.get("category")
        difficulty = request.args.get("difficulty")

        from ..models.learning import LearningManager

        lm = LearningManager()

        courses = lm.get_courses(
            user_id=user_id,
            category=category,
            difficulty=difficulty,
            published_only=True,
        )

        return jsonify({"success": True, "data": [c.to_dict() for c in courses]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/courses", methods=["POST"])
def create_course():
    """Create a new course (teacher only)"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager

        lm = LearningManager()

        course = lm.create_course(
            user_id=user_id,
            title=data.get("title"),
            description=data.get("description", ""),
            category=data.get("category", "general"),
            difficulty=data.get("difficulty", "beginner"),
            duration_hours=float(data.get("duration_hours", 1)),
            modules=data.get("modules", []),
        )

        return jsonify({"success": True, "data": course.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    """Get course details"""
    try:
        from ..models.learning import LearningManager

        lm = LearningManager()

        courses = lm.get_courses(published_only=False)
        course = next((c for c in courses if c.course_id == course_id), None)

        if not course:
            return jsonify({"success": False, "error": "Course not found"}), 404

        return jsonify({"success": True, "data": course.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/courses/<course_id>", methods=["PUT"])
def update_course(course_id):
    """Update course"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager

        lm = LearningManager()

        courses = lm.get_courses(user_id=user_id, published_only=False)
        course = next((c for c in courses if c.course_id == course_id), None)

        if not course:
            return jsonify({"success": False, "error": "Course not found"}), 404

        lm.update_course(course_id, **data)

        return jsonify({"success": True, "message": "Course updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/courses/<course_id>/publish", methods=["POST"])
def publish_course(course_id):
    """Publish a course"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.learning import LearningManager

        lm = LearningManager()

        courses = lm.get_courses(user_id=user_id, published_only=False)
        course = next((c for c in courses if c.course_id == course_id), None)

        if not course:
            return jsonify({"success": False, "error": "Course not found"}), 404

        lm.update_course(course_id, is_published=True)

        return jsonify({"success": True, "message": "Course published"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/enrollments", methods=["GET"])
def get_enrollments():
    """Get user enrollments"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        course_id = request.args.get("course_id")

        from ..models.learning import LearningManager

        lm = LearningManager()

        enrollments = lm.get_enrollments(student_id=user_id, course_id=course_id)

        # Add course info
        courses = lm.get_courses(published_only=False)

        for enrollment in enrollments:
            course = next(
                (c for c in courses if c.course_id == enrollment.course_id), None
            )
            if course:
                enrollment.course_title = course.title

        return jsonify({"success": True, "data": [e.to_dict() for e in enrollments]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/enrollments", methods=["POST"])
def enroll_student():
    """Enroll in a course"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager

        lm = LearningManager()

        # Check if already enrolled
        existing = lm.get_enrollments(
            student_id=user_id, course_id=data.get("course_id")
        )
        if existing:
            return jsonify({"success": False, "error": "Already enrolled"}), 400

        enrollment = lm.enroll_student(
            course_id=data.get("course_id"), student_id=user_id
        )

        return jsonify({"success": True, "data": enrollment.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/progress/<enrollment_id>", methods=["POST"])
def update_progress(enrollment_id):
    """Update lesson progress"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager

        lm = LearningManager()

        lm.update_progress(
            enrollment_id=enrollment_id,
            lesson_id=data.get("lesson_id"),
            completed=data.get("completed", False),
            time_spent=data.get("time_spent", 0),
            quiz_score=data.get("quiz_score"),
        )

        return jsonify({"success": True, "message": "Progress updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/tutoring", methods=["GET"])
def get_tutoring_sessions():
    """Get tutoring sessions"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.learning import LearningManager

        lm = LearningManager()

        sessions = lm.get_sessions(student_id=user_id)

        return jsonify({"success": True, "data": [s.to_dict() for s in sessions]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/tutoring", methods=["POST"])
def create_tutoring_session():
    """Create a new tutoring session"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager

        lm = LearningManager()

        session = lm.create_tutoring_session(
            student_id=user_id,
            course_id=data.get("course_id"),
            topic=data.get("topic", ""),
        )

        return jsonify({"success": True, "data": session.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/tutoring/<session_id>/message", methods=["POST"])
def send_tutoring_message(session_id):
    """Send a message in tutoring session"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        data = request.get_json()

        from ..models.learning import LearningManager
        from ..services.ai_services import LearningRecommender

        lm = LearningManager()

        # Add user message
        lm.add_message(session_id, "user", data.get("message", ""))

        # Get session context
        sessions = lm.get_sessions(student_id=user_id)
        session = next((s for s in sessions if s.session_id == session_id), None)

        if not session:
            return jsonify({"success": False, "error": "Session not found"}), 404

        # Generate AI response (simplified - could integrate with LLM)
        ai_response = f"Got your message about: {data.get('message', '')}. I'm here to help with your learning journey. What specific topic would you like to explore?"

        # Add AI response
        lm.add_message(session_id, "assistant", ai_response)

        return jsonify(
            {"success": True, "data": {"message": ai_response, "role": "assistant"}}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    """Get course recommendations"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        interests = request.args.get("interests", "").split(",")
        skill_level = request.args.get("skill_level", "beginner")

        from ..services.ai_services import LearningRecommender

        recommender = LearningRecommender()

        recommendations = recommender.recommend_courses(
            user_id=user_id, interests=interests, skill_level=skill_level
        )

        return jsonify({"success": True, "data": recommendations})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/study-plan/<course_id>", methods=["GET"])
def get_study_plan(course_id):
    """Get personalized study plan"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        hours = float(request.args.get("hours_per_week", 5))

        from ..services.ai_services import LearningRecommender

        recommender = LearningRecommender()

        plan = recommender.generate_study_plan(course_id, hours)

        return jsonify({"success": True, "data": plan})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@learning_bp.route("/learning-paths", methods=["GET"])
def get_learning_paths():
    """Get learning paths"""
    try:
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return jsonify({"success": False, "error": "Authentication required"}), 401

        from ..models.learning import LearningManager

        lm = LearningManager()

        paths = lm.get_learning_paths(user_id)

        return jsonify({"success": True, "data": [p.to_dict() for p in paths]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
