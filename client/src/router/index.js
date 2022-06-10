import Vue from 'vue';
import VueRouter from 'vue-router';
import CourseList from "../views/CourseList";
import UnitList from "../views/UnitList";
import LessonList from "../views/LessonList";
import Lesson from "../views/Lesson/LessonController";
import Login from "../views/Login";
import GoogleLoginCallback from "../views/GoogleLoginCallback";
import ClassManagement from "../views/ClassManagement";
import Accounts from "../views/Accounts";
import Schools from "../views/Schools";

Vue.use(VueRouter);

const routes = [
  {
    name: 'login',
    path: '/login',
    component: Login,
    props: true
  },
  {
    name: 'dashboard',
    path: '/',
    component: CourseList,
  },
  {
    name: 'course_detail',
    path: '/course/:courseId',
    component: UnitList,
    props: true
  },
  {
    name: 'unit_detail',
    path: '/unit/:unitId',
    component: LessonList,
    props: true
  },
  {
    name: 'lesson_detail',
    path: '/lesson/:lessonId',
    component: Lesson,
    props: true
  },
  {
    name: 'class_management',
    path: '/classes',
    component: ClassManagement
  },
  {
    name: 'account_management',
    path: '/accounts',
    component: Accounts
  },
  {
    name: 'school_management',
    path: '/schools',
    component: Schools
  }
];

const router = new VueRouter({
  routes,
});

export default router;
