# Database & ORM Audit Report
**Generated:** 2025-07-24T22:28:27.667697

## Executive Summary

- **Total Models:** 25
- **Total Issues:** 92
- **High Severity:** 51
- **Medium Severity:** 41
- **Low Severity:** 0

## Models Discovered

### Student
- **Table:** `students`
- **Columns:** 13
- **Relationships:** 2

### LearningSession
- **Table:** `learning_sessions`
- **Columns:** 15
- **Relationships:** 0

### Assessment
- **Table:** `assessments`
- **Columns:** 14
- **Relationships:** 0

### ARIAInteraction
- **Table:** `aria_interactions`
- **Columns:** 10
- **Relationships:** 0

### User
- **Table:** `users`
- **Columns:** 19
- **Relationships:** 5

### StudentProfile
- **Table:** `student_profiles`
- **Columns:** 14
- **Relationships:** 0

### ParentProfile
- **Table:** `parent_profiles`
- **Columns:** 11
- **Relationships:** 0

### TeacherProfile
- **Table:** `teacher_profiles`
- **Columns:** 24
- **Relationships:** 0

### AdminProfile
- **Table:** `admin_profiles`
- **Columns:** 11
- **Relationships:** 0

### UserSession
- **Table:** `user_sessions`
- **Columns:** 12
- **Relationships:** 0

### ParentChildRelation
- **Table:** `parent_child_relations`
- **Columns:** 10
- **Relationships:** 0

### Formula
- **Table:** `formulas`
- **Columns:** 13
- **Relationships:** 1

### Location
- **Table:** `locations`
- **Columns:** 8
- **Relationships:** 1

### Availability
- **Table:** `availabilities`
- **Columns:** 10
- **Relationships:** 0

### Booking
- **Table:** `bookings`
- **Columns:** 20
- **Relationships:** 1

### SessionReport
- **Table:** `session_reports`
- **Columns:** 12
- **Relationships:** 0

### Group
- **Table:** `groups`
- **Columns:** 11
- **Relationships:** 2

### Teacher
- **Table:** `teachers`
- **Columns:** 15
- **Relationships:** 5

### Enrollment
- **Table:** `enrollments`
- **Columns:** 10
- **Relationships:** 0

### IndividualSession
- **Table:** `individual_sessions`
- **Columns:** 15
- **Relationships:** 0

### GroupSession
- **Table:** `group_sessions`
- **Columns:** 13
- **Relationships:** 1

### SessionAttendance
- **Table:** `session_attendances`
- **Columns:** 7
- **Relationships:** 0

### WeeklyReport
- **Table:** `weekly_reports`
- **Columns:** 11
- **Relationships:** 0

### ParentCommunication
- **Table:** `parent_communications`
- **Columns:** 11
- **Relationships:** 0

### StudentObjective
- **Table:** `student_objectives`
- **Columns:** 11
- **Relationships:** 0

## 🔴 High Severity Issues

### LearningSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_learning_sessions_student_id ON learning_sessions(student_id);`

### Assessment
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_assessments_student_id ON assessments(student_id);`

### ARIAInteraction
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_aria_interactions_student_id ON aria_interactions(student_id);`

### StudentProfile
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_profiles_user_id ON student_profiles(user_id);`

### ParentProfile
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_profiles_user_id ON parent_profiles(user_id);`

### TeacherProfile
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_teacher_profiles_user_id ON teacher_profiles(user_id);`

### AdminProfile
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_admin_profiles_user_id ON admin_profiles(user_id);`

### UserSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);`

### ParentChildRelation
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_child_relations_parent_user_id ON parent_child_relations(parent_user_id);`

### ParentChildRelation
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_child_relations_child_user_id ON parent_child_relations(child_user_id);`

### Availability
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_availabilities_teacher_id ON availabilities(teacher_id);`

### Booking
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_student_id ON bookings(student_id);`

### Booking
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_teacher_id ON bookings(teacher_id);`

### Booking
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_availability_id ON bookings(availability_id);`

### Booking
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_location_id ON bookings(location_id);`

### SessionReport
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_reports_booking_id ON session_reports(booking_id);`

### SessionReport
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_reports_teacher_id ON session_reports(teacher_id);`

### Group
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_groups_teacher_id ON groups(teacher_id);`

### Group
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_groups_default_location_id ON groups(default_location_id);`

### Enrollment
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);`

### Enrollment
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_enrollments_formula_id ON enrollments(formula_id);`

### Enrollment
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_enrollments_group_id ON enrollments(group_id);`

### Enrollment
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_enrollments_teacher_id ON enrollments(teacher_id);`

### IndividualSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_individual_sessions_student_id ON individual_sessions(student_id);`

### IndividualSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_individual_sessions_teacher_id ON individual_sessions(teacher_id);`

### IndividualSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_individual_sessions_location_id ON individual_sessions(location_id);`

### GroupSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_group_sessions_group_id ON group_sessions(group_id);`

### GroupSession
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_group_sessions_location_id ON group_sessions(location_id);`

### SessionAttendance
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_attendances_session_id ON session_attendances(session_id);`

### SessionAttendance
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_attendances_student_id ON session_attendances(student_id);`

### WeeklyReport
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_weekly_reports_student_id ON weekly_reports(student_id);`

### ParentCommunication
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_communications_student_id ON parent_communications(student_id);`

### StudentObjective
- **Type:** missing_index
- **Issue:** Foreign key without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_objectives_student_id ON student_objectives(student_id);`

### Student
- **Type:** n_plus_one_risk
- **Issue:** Relationship Student.sessions uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for sessions

### Student
- **Type:** n_plus_one_risk
- **Issue:** Relationship Student.assessments uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for assessments

### User
- **Type:** n_plus_one_risk
- **Issue:** Relationship User.student_profile uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for student_profile

### User
- **Type:** n_plus_one_risk
- **Issue:** Relationship User.parent_profile uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for parent_profile

### User
- **Type:** n_plus_one_risk
- **Issue:** Relationship User.teacher_profile uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for teacher_profile

### User
- **Type:** n_plus_one_risk
- **Issue:** Relationship User.admin_profile uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for admin_profile

### User
- **Type:** n_plus_one_risk
- **Issue:** Relationship User.user_sessions uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for user_sessions

### Formula
- **Type:** n_plus_one_risk
- **Issue:** Relationship Formula.enrollments uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for enrollments

### Location
- **Type:** n_plus_one_risk
- **Issue:** Relationship Location.bookings uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for bookings

### Booking
- **Type:** n_plus_one_risk
- **Issue:** Relationship Booking.session_report uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for session_report

### Group
- **Type:** n_plus_one_risk
- **Issue:** Relationship Group.enrollments uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for enrollments

### Group
- **Type:** n_plus_one_risk
- **Issue:** Relationship Group.sessions uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for sessions

### Teacher
- **Type:** n_plus_one_risk
- **Issue:** Relationship Teacher.groups uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for groups

### Teacher
- **Type:** n_plus_one_risk
- **Issue:** Relationship Teacher.individual_sessions uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for individual_sessions

### Teacher
- **Type:** n_plus_one_risk
- **Issue:** Relationship Teacher.availabilities uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for availabilities

### Teacher
- **Type:** n_plus_one_risk
- **Issue:** Relationship Teacher.bookings uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for bookings

### Teacher
- **Type:** n_plus_one_risk
- **Issue:** Relationship Teacher.session_reports uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for session_reports

### GroupSession
- **Type:** n_plus_one_risk
- **Issue:** Relationship GroupSession.attendances uses lazy='select'
- **Recommendation:** Consider using lazy='joined' or lazy='subquery' for attendances

## 🟡 Medium Severity Issues

### Student
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_students_created_at ON students(created_at);`

### Student
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_students_updated_at ON students(updated_at);`

### LearningSession
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_learning_sessions_created_at ON learning_sessions(created_at);`

### Assessment
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_assessments_created_at ON assessments(created_at);`

### ARIAInteraction
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_aria_interactions_created_at ON aria_interactions(created_at);`

### User
- **Type:** missing_index
- **Issue:** Common query field "status" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_users_status ON users(status);`

### User
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_users_created_at ON users(created_at);`

### User
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_users_updated_at ON users(updated_at);`

### StudentProfile
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_profiles_created_at ON student_profiles(created_at);`

### StudentProfile
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_profiles_updated_at ON student_profiles(updated_at);`

### ParentProfile
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_profiles_created_at ON parent_profiles(created_at);`

### ParentProfile
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_profiles_updated_at ON parent_profiles(updated_at);`

### TeacherProfile
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_teacher_profiles_created_at ON teacher_profiles(created_at);`

### TeacherProfile
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_teacher_profiles_updated_at ON teacher_profiles(updated_at);`

### AdminProfile
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_admin_profiles_created_at ON admin_profiles(created_at);`

### AdminProfile
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_admin_profiles_updated_at ON admin_profiles(updated_at);`

### UserSession
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_user_sessions_created_at ON user_sessions(created_at);`

### ParentChildRelation
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_child_relations_created_at ON parent_child_relations(created_at);`

### Formula
- **Type:** missing_index
- **Issue:** Common query field "type" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_formulas_type ON formulas(type);`

### Formula
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_formulas_created_at ON formulas(created_at);`

### Formula
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_formulas_updated_at ON formulas(updated_at);`

### Location
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_locations_created_at ON locations(created_at);`

### Location
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_locations_updated_at ON locations(updated_at);`

### Availability
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_availabilities_created_at ON availabilities(created_at);`

### Availability
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_availabilities_updated_at ON availabilities(updated_at);`

### Booking
- **Type:** missing_index
- **Issue:** Common query field "status" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_status ON bookings(status);`

### Booking
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_created_at ON bookings(created_at);`

### Booking
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_bookings_updated_at ON bookings(updated_at);`

### SessionReport
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_reports_created_at ON session_reports(created_at);`

### Group
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_groups_created_at ON groups(created_at);`

### Teacher
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_teachers_created_at ON teachers(created_at);`

### Enrollment
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_enrollments_created_at ON enrollments(created_at);`

### IndividualSession
- **Type:** missing_index
- **Issue:** Common query field "status" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_individual_sessions_status ON individual_sessions(status);`

### IndividualSession
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_individual_sessions_created_at ON individual_sessions(created_at);`

### GroupSession
- **Type:** missing_index
- **Issue:** Common query field "status" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_group_sessions_status ON group_sessions(status);`

### GroupSession
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_group_sessions_created_at ON group_sessions(created_at);`

### SessionAttendance
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_session_attendances_created_at ON session_attendances(created_at);`

### WeeklyReport
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_weekly_reports_created_at ON weekly_reports(created_at);`

### ParentCommunication
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_parent_communications_created_at ON parent_communications(created_at);`

### StudentObjective
- **Type:** missing_index
- **Issue:** Common query field "created_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_objectives_created_at ON student_objectives(created_at);`

### StudentObjective
- **Type:** missing_index
- **Issue:** Common query field "updated_at" without index
- **Recommendation:** N/A
- **SQL:** `CREATE INDEX idx_student_objectives_updated_at ON student_objectives(updated_at);`

## Database Schema (DBML)

```dbml
// Nexus Réussite Database Schema
// Generated on 2025-07-24 22:28:27

Table students {
  id int [pk]
  full_name varchar [not null]
  email varchar [not null, unique]
  phone varchar
  grade_level varchar [not null]
  school varchar
  preferred_subjects text
  learning_style varchar
  cognitive_profile text
  performance_data text
  created_at datetime
  updated_at datetime
  is_active boolean
}

Table learning_sessions {
  id int [pk]
  student_id int [not null]
  subject varchar [not null]
  topic varchar [not null]
  session_type varchar [not null]
  duration_minutes int
  aria_recommendations text
  interaction_data text
  performance_metrics text
  completion_rate float
  accuracy_rate float
  difficulty_level varchar
  started_at datetime
  completed_at datetime
  created_at datetime
}

Table assessments {
  id int [pk]
  student_id int [not null]
  title varchar [not null]
  subject varchar [not null]
  assessment_type varchar [not null]
  questions_data text [not null]
  answers_data text
  score float
  detailed_results text
  aria_feedback text
  next_steps text
  created_at datetime
  completed_at datetime
  is_completed boolean
}

Table aria_interactions {
  id int [pk]
  student_id int [not null]
  interaction_type varchar [not null]
  user_input text
  aria_response text [not null]
  context_data text
  confidence_score float
  processing_time_ms int
  feedback_rating int
  created_at datetime
}

Table users {
  id int [pk]
  email varchar [not null, unique]
  password_hash varchar [not null]
  first_name varchar [not null]
  last_name varchar [not null]
  phone varchar
  avatar_url varchar
  role varchar [not null]
  status varchar
  last_login datetime
  email_verified boolean
  email_verification_token varchar
  password_reset_token varchar
  password_reset_expires datetime
  preferences json
  timezone varchar
  language varchar
  created_at datetime
  updated_at datetime
}

Table student_profiles {
  id int [pk]
  user_id int [not null, unique]
  grade_level varchar [not null]
  school varchar
  specialties json
  learning_style varchar
  cognitive_profile json
  performance_data json
  goals json
  interests json
  motivation_level varchar
  parent_ids json
  created_at datetime
  updated_at datetime
}

Table parent_profiles {
  id int [pk]
  user_id int [not null, unique]
  profession varchar
  address text
  emergency_contact varchar
  children_ids json
  preferred_contact_method varchar
  notification_preferences json
  report_frequency varchar
  created_at datetime
  updated_at datetime
}

Table teacher_profiles {
  id int [pk]
  user_id int [not null, unique]
  subjects json [not null]
  qualifications json
  experience_years int
  is_aefe_certified boolean
  is_nsi_diu boolean
  can_teach_online boolean
  can_teach_in_person boolean
  preferred_formats json
  hourly_rate_online float
  hourly_rate_in_person float
  hourly_rate_group float
  default_availability json
  max_hours_per_week int
  rating float
  total_reviews int
  total_hours_taught int
  bio text
  specialties_description text
  hire_date varchar
  is_active_teacher boolean
  created_at datetime
  updated_at datetime
}

Table admin_profiles {
  id int [pk]
  user_id int [not null, unique]
  permissions json
  department varchar
  is_super_admin boolean
  can_manage_users boolean
  can_manage_content boolean
  can_view_reports boolean
  can_manage_billing boolean
  created_at datetime
  updated_at datetime
}

Table user_sessions {
  id int [pk]
  user_id int [not null]
  session_token varchar [not null, unique]
  refresh_token varchar [unique]
  expires_at datetime [not null]
  ip_address varchar
  user_agent varchar
  device_type varchar
  location varchar
  is_active boolean
  last_activity datetime
  created_at datetime
}

Table parent_child_relations {
  id int [pk]
  parent_user_id int [not null]
  child_user_id int [not null]
  relation_type varchar
  is_primary_contact boolean
  can_view_grades boolean
  can_book_sessions boolean
  can_receive_reports boolean
  confirmed_at datetime
  created_at datetime
}

Table formulas {
  id int [pk]
  name varchar [not null]
  type varchar [not null]
  level varchar [not null]
  price_dt float [not null]
  hours_per_month int [not null]
  max_students int
  description text
  features json
  supports_online boolean
  supports_in_person boolean
  created_at datetime
  updated_at datetime
}

Table locations {
  id int [pk]
  name varchar [not null]
  capacity int [not null]
  address varchar
  equipment json
  is_active boolean
  created_at datetime
  updated_at datetime
}

Table availabilities {
  id int [pk]
  teacher_id int [not null]
  start_time datetime [not null]
  end_time datetime [not null]
  is_for_in_person boolean [not null]
  is_recurring boolean
  recurring_pattern json
  is_booked boolean
  created_at datetime
  updated_at datetime
}

Table bookings {
  id int [pk]
  student_id int [not null]
  teacher_id int [not null]
  availability_id int
  start_time datetime [not null]
  end_time datetime [not null]
  format varchar [not null]
  location_id int
  subject varchar [not null]
  topic varchar
  description text
  duration_minutes int
  status varchar
  booking_notes text
  cancellation_reason varchar
  meeting_url varchar
  meeting_password varchar
  created_at datetime
  updated_at datetime
  created_by varchar
}

Table session_reports {
  id int [pk]
  booking_id int [not null]
  topics_covered json
  student_performance int
  participation_level varchar
  comprehension_level varchar
  teacher_notes text
  homework_assigned text
  next_session_recommendations text
  parent_feedback_requested boolean
  created_at datetime
  teacher_id int [not null]
}

Table groups {
  id int [pk]
  name varchar [not null]
  subject varchar [not null]
  level varchar [not null]
  max_students int
  current_students int
  teacher_id int [not null]
  default_location_id int
  supports_online boolean
  schedule json
  created_at datetime
}

Table teachers {
  id int [pk]
  first_name varchar [not null]
  last_name varchar [not null]
  email varchar [not null, unique]
  phone varchar
  subjects json
  qualifications json
  experience_years int
  is_aefe_certified boolean
  is_nsi_diu boolean
  can_teach_online boolean
  can_teach_in_person boolean
  hourly_rate_online float
  hourly_rate_in_person float
  created_at datetime
}

Table enrollments {
  id int [pk]
  student_id int [not null]
  formula_id int [not null]
  group_id int
  teacher_id int
  start_date varchar [not null]
  end_date varchar
  is_active boolean
  preferred_format varchar
  created_at datetime
}

Table individual_sessions {
  id int [pk]
  student_id int [not null]
  teacher_id int [not null]
  subject varchar [not null]
  scheduled_at datetime [not null]
  duration_minutes int
  format varchar
  location_id int
  status varchar
  topics_covered json
  homework_assigned text
  teacher_notes text
  student_performance int
  meeting_url varchar
  created_at datetime
}

Table group_sessions {
  id int [pk]
  group_id int [not null]
  subject varchar [not null]
  scheduled_at datetime [not null]
  duration_minutes int
  format varchar
  location_id int
  status varchar
  topics_covered json
  homework_assigned text
  teacher_notes text
  meeting_url varchar
  created_at datetime
}

Table session_attendances {
  id int [pk]
  session_id int [not null]
  student_id int [not null]
  is_present boolean
  participation_score int
  individual_notes text
  created_at datetime
}

Table weekly_reports {
  id int [pk]
  student_id int [not null]
  week_start_date varchar [not null]
  week_end_date varchar [not null]
  subjects_progress json
  aria_insights text
  teacher_comments json
  next_week_objectives json
  parent_feedback text
  is_sent_to_parents boolean
  created_at datetime
}

Table parent_communications {
  id int [pk]
  student_id int [not null]
  sender_type varchar [not null]
  sender_id int [not null]
  recipient_type varchar [not null]
  recipient_id int [not null]
  subject varchar [not null]
  message text [not null]
  is_read boolean
  priority varchar
  created_at datetime
}

Table student_objectives {
  id int [pk]
  student_id int [not null]
  subject varchar [not null]
  objective_text text [not null]
  target_date varchar [not null]
  is_achieved boolean
  achievement_date varchar
  progress_percentage int
  created_by varchar [not null]
  created_at datetime
  updated_at datetime
}

// Relationships
Ref: learning_sessions.student_id > students.id
Ref: assessments.student_id > students.id
Ref: aria_interactions.student_id > students.id
Ref: student_profiles.user_id > users.id
Ref: parent_profiles.user_id > users.id
Ref: teacher_profiles.user_id > users.id
Ref: admin_profiles.user_id > users.id
Ref: user_sessions.user_id > users.id
Ref: parent_child_relations.parent_user_id > parent_users.id
Ref: parent_child_relations.child_user_id > child_users.id
Ref: availabilities.teacher_id > teachers.id
Ref: bookings.student_id > students.id
Ref: bookings.teacher_id > teachers.id
Ref: bookings.availability_id > availabilitys.id
Ref: bookings.location_id > locations.id
Ref: session_reports.booking_id > bookings.id
Ref: session_reports.teacher_id > teachers.id
Ref: groups.teacher_id > teachers.id
Ref: groups.default_location_id > default_locations.id
Ref: enrollments.student_id > students.id
Ref: enrollments.formula_id > formulas.id
Ref: enrollments.group_id > groups.id
Ref: enrollments.teacher_id > teachers.id
Ref: individual_sessions.student_id > students.id
Ref: individual_sessions.teacher_id > teachers.id
Ref: individual_sessions.location_id > locations.id
Ref: group_sessions.group_id > groups.id
Ref: group_sessions.location_id > locations.id
Ref: session_attendances.session_id > sessions.id
Ref: session_attendances.student_id > students.id
Ref: weekly_reports.student_id > students.id
Ref: parent_communications.student_id > students.id
Ref: student_objectives.student_id > students.id
```